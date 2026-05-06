-- =========================================
-- SISTEMA COMPLETO: ESTOQUE + VENDAS + FINANCEIRO
-- =========================================

CREATE DATABASE IF NOT EXISTS estoque;
USE estoque;

-- ================= PRODUTOS =================
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    saldo INT DEFAULT 0,
    custo_medio DECIMAL(10,2) DEFAULT 0
);

-- ================= COMPRAS =================
CREATE TABLE IF NOT EXISTS compras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('PENDENTE', 'RECEBIDO') DEFAULT 'PENDENTE'
);

CREATE TABLE IF NOT EXISTS itens_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT,
    produto_id INT,
    quantidade INT NOT NULL,
    custo_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (compra_id) REFERENCES compras(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- ================= MOVIMENTACOES =================
CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    tipo ENUM('ENTRADA', 'SAIDA'),
    quantidade INT,
    custo_unitario DECIMAL(10,2),
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- ================= CLIENTES =================
CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100)
);

-- ================= VENDAS =================
CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    data DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS itens_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT,
    produto_id INT,
    quantidade INT,
    preco_unitario DECIMAL(10,2),
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

-- ================= FINANCEIRO =================
CREATE TABLE IF NOT EXISTS contas_receber (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venda_id INT,
    valor DECIMAL(10,2),
    data_vencimento DATE,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    FOREIGN KEY (venda_id) REFERENCES vendas(id)
);

CREATE TABLE IF NOT EXISTS contas_pagar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    compra_id INT,
    valor DECIMAL(10,2),
    data_vencimento DATE,
    status VARCHAR(20) DEFAULT 'PENDENTE',
    FOREIGN KEY (compra_id) REFERENCES compras(id)
);

-- ================= PROCEDURE COMPRA =================
DROP PROCEDURE IF EXISTS confirmar_compra;
DELIMITER $$

CREATE PROCEDURE confirmar_compra(p_compra_id INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_produto_id INT;
    DECLARE v_qtd INT;
    DECLARE v_custo DECIMAL(10,2);
    DECLARE v_saldo INT;
    DECLARE v_custo_medio DECIMAL(10,2);

    DECLARE cur CURSOR FOR 
        SELECT produto_id, quantidade, custo_unitario
        FROM itens_compra
        WHERE compra_id = p_compra_id;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_produto_id, v_qtd, v_custo;
        IF done THEN LEAVE read_loop; END IF;

        SELECT saldo, custo_medio INTO v_saldo, v_custo_medio
        FROM produtos WHERE id = v_produto_id;

        SET @novo_custo = 
        ((v_saldo * v_custo_medio) + (v_qtd * v_custo)) 
        / (v_saldo + v_qtd);

        UPDATE produtos
        SET saldo = saldo + v_qtd,
            custo_medio = @novo_custo
        WHERE id = v_produto_id;

        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, custo_unitario)
        VALUES (v_produto_id, 'ENTRADA', v_qtd, v_custo);

    END LOOP;

    CLOSE cur;

    UPDATE compras SET status = 'RECEBIDO' WHERE id = p_compra_id;

    COMMIT;
END$$

-- ================= PROCEDURE VENDA =================
DROP PROCEDURE IF EXISTS realizar_venda;

CREATE PROCEDURE realizar_venda(p_venda_id INT)
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE v_produto_id INT;
    DECLARE v_qtd INT;
    DECLARE v_preco DECIMAL(10,2);
    DECLARE v_saldo INT;

    DECLARE cur CURSOR FOR 
        SELECT produto_id, quantidade, preco_unitario
        FROM itens_venda
        WHERE venda_id = p_venda_id;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    START TRANSACTION;

    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO v_produto_id, v_qtd, v_preco;
        IF done THEN LEAVE read_loop; END IF;

        SELECT saldo INTO v_saldo FROM produtos WHERE id = v_produto_id;

        IF v_saldo < v_qtd THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Estoque insuficiente!';
        END IF;

        UPDATE produtos SET saldo = saldo - v_qtd WHERE id = v_produto_id;

        INSERT INTO movimentacoes_estoque
        (produto_id, tipo, quantidade, custo_unitario)
        VALUES (v_produto_id, 'SAIDA', v_qtd, v_preco);

    END LOOP;

    CLOSE cur;

    INSERT INTO contas_receber (venda_id, valor, data_vencimento)
    SELECT v.id, SUM(iv.quantidade * iv.preco_unitario), CURDATE()
    FROM vendas v
    JOIN itens_venda iv ON v.id = iv.venda_id
    WHERE v.id = p_venda_id;

    COMMIT;
END$$

DELIMITER ;

-- ================= TESTES =================

INSERT INTO produtos (nome, saldo, custo_medio)
VALUES ('Produto A', 10, 5.00);

INSERT INTO compras () VALUES ();
INSERT INTO itens_compra (compra_id, produto_id, quantidade, custo_unitario)
VALUES (1, 1, 10, 7.00);

CALL confirmar_compra(1);

INSERT INTO clientes (nome) VALUES ('João');
INSERT INTO vendas (cliente_id) VALUES (1);
INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
VALUES (1, 1, 5, 10.00);

CALL realizar_venda(1);

SELECT * FROM produtos;
SELECT * FROM contas_receber;

-- ================= RELATORIO =================
SELECT 
    SUM(iv.preco_unitario * iv.quantidade) AS faturamento,
    SUM(p.custo_medio * iv.quantidade) AS custo,
    SUM((iv.preco_unitario - p.custo_medio) * iv.quantidade) AS lucro
FROM itens_venda iv
JOIN produtos p ON iv.produto_id = p.id;
