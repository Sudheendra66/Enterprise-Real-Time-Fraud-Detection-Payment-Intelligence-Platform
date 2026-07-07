{% macro fraud_rate() %}
round(
100.0 * sum(fraud_prediction) / count(*),
2
)
{% endmacro %}

{% macro fraud_amount() %}
sum(
case
when fraud_prediction = 1
then TransactionAmt
else 0
end
)
{% endmacro %}

{% macro high_risk_transactions() %}
sum(fraud_prediction)
{% endmacro %}