# Sprint 3 (недели 5-6): Reliability v1

## Цель спринта

Повысить надежность исполнения за счет формальной taxonomy отказов, автовосстановления и safe-state поведения.

## Объем работ

- Failure taxonomy: sensor, planner, execution, integration
- Автовосстановление для критичных кейсов
- Safe-state policy (stop/park/notify)
- Нагрузочные прогоны и статистика надежности

## Технические задачи

- Утвердить матрицу отказов и mapping "класс отказа -> реакция policy"
- Добавить recovery-strategy per failure class
- Реализовать safe-state policy с минимумом небезопасных переходов
- Запустить серию длительных прогонов: **PyBullet** (массовые/headless) и выборочно **Webots** (реалистичные сцены)
- Сформировать reliability baseline по метрикам

## Артефакт спринта

- Отчет `reliability baseline` с численными результатами и ограничениями

## Definition of Done

- Все 4 класса отказов обрабатываются через единый policy layer
- Для критичных отказов включено и подтверждено автовосстановление
- Safe-state сценарии покрыты тестами и не ломают lifecycle
- Reliability-отчет содержит динамику success rate / MTTR / interventions

## KPI контроля

- Mission success rate под нагрузкой
- MTTR по классам отказов
- Auto-recovery rate по критичным кейсам
- Manual interventions per N missions

## Зависимости

- Оркестрация и incident logging из Sprint 2
- Достаточный набор тестовых failure-сценариев

## Риски и снижение

- Риск: рост сложности policy ухудшит предсказуемость  
  Митигирование: policy ruleset с явным приоритетом правил
- Риск: метрики искажаются флаки-тестами  
  Митигирование: фиксированные seeds и прогон сериями
