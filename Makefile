# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rvaz-da- <rvaz-da-@student.s19.be>         +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/04/14 11:52:09 by rvaz-da-          #+#    #+#              #
#    Updated: 2026/04/14 11:52:10 by rvaz-da-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = fly_in.py
VENV = .venv
PY = python

install:
	uv python install 3.12
	uv sync
	@echo Virtual environment setup complete!

run:
	uv run $(PY) $(NAME)

debug:
	uv run $(PY) -m pdb $(NAME)

lint:
	uv run flake8 .
	uv run mypy .

lint-strict:
	uv run flake8 .
	uv run mypy --strict .

clean:
	rm -rf __pycache__/
	rm -rf .mypy_cache/
	rm -rf .pytest_cache
	find . -type f -name "*.pyc" -delete
	@echo Project cleanup complete!

fclean: clean
	rm -rf .venv/
	@echo Project reset complete

re: clean run

.PHONY: install run debug lint lint-strict clean fclean re