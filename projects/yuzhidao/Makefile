.PHONY: help db-init collect-year collect-price collect-customs dashboard test clean

PROJECT_DIR := $(shell pwd)
PYTHON := python3

help:
	@echo "海参行业数据收集平台 - 可用命令"
	@echo "================================"
	@echo "make db-init        - 初始化数据库"
	@echo "make collect-year   - 执行年度数据采集（渔业统计）"
	@echo "make collect-price  - 执行价格数据采集"
	@echo "make collect-customs- 执行海关数据采集"
	@echo "make dashboard      - 启动Streamlit看板"
	@echo "make test           - 测试数据采集脚本"
	@echo "make clean          - 清理临时文件"

db-init:
	$(PYTHON) -c "from src.database import init_db; init_db()"
	@echo "数据库初始化完成"

collect-year:
	$(PYTHON) scripts/collect_fishery_stats.py --year $$(date +%Y)

collect-price:
	$(PYTHON) scripts/collect_price.py

collect-customs:
	$(PYTHON) scripts/collect_customs.py --year $$(date +%Y)

dashboard:
	streamlit run dashboard/app.py --server.port 8501 --server.headless true

test:
	$(PYTHON) -c "from src.database import init_db, get_production_data; init_db(); print(get_production_data())"

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf data/raw/*/ 2>/dev/null || true
	@echo "清理完成"
