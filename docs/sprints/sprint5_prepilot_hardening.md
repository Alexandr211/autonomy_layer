# Sprint 5 (недели 9-10): Pre-pilot Hardening I

## Цель спринта

Снизить операционные риски перед пилотом через усиление regression/fault-injection и ускорение восстановления.

## Объем работ

- Улучшение MTTR и снижение ручных вмешательств
- Расширение regression suite
- Расширенный fault injection

## Технические задачи

- Выделить top-ошибки по частоте и влиянию
- Добавить targeted recovery-правила под эти ошибки
- Расширить regression-набор по критичным путям
- Добавить сценарии составных сбоев в fault injection

## Артефакт спринта

- Hardening report I: что улучшено, что осталось в рисках

## Definition of Done

- MTTR снижен относительно baseline Sprint 3
- Manual interventions по топ-сценариям снижены
- Regression suite покрывает ключевые отказоустойчивые пути
- Расширенный fault injection встроен в CI/регулярный прогон

## KPI контроля

- Delta MTTR к baseline
- Delta manual interventions
- Regression pass rate

## Зависимости

- API/packaging и reliability-данные из Sprint 4

## Риски и снижение

- Риск: рост времени регресса  
  Митигирование: tiered test strategy (smoke/nightly/full)
