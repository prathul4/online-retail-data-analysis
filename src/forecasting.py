"""Monthly revenue forecasting with a Holt-Winters exponential smoothing
model, backtested against the most recent months before refitting on the
full series for a genuine forward forecast.
"""

import calendar

import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing

from src import config, visualize

FORECAST_HORIZON = config.FORECAST_HOLDOUT_MONTHS


def _to_monthly_series(monthly_kpis):
    series = monthly_kpis.set_index("YearMonth")["Total_Revenue"].copy()
    series.index = pd.PeriodIndex(series.index, freq="M").to_timestamp()
    return series


def _is_partial_month(max_invoice_date):
    days_in_month = calendar.monthrange(max_invoice_date.year, max_invoice_date.month)[1]
    return max_invoice_date.day < days_in_month


def forecast_revenue(monthly_kpis, max_invoice_date=None):
    series = _to_monthly_series(monthly_kpis)

    excluded_partial_month = None
    if max_invoice_date is not None and _is_partial_month(max_invoice_date):
        excluded_partial_month = series.index[-1]
        series = series.iloc[:-1]

    if len(series) <= FORECAST_HORIZON + 2:
        # Not enough history for a meaningful holdout; skip backtesting.
        mape = None
    else:
        train, test = series.iloc[:-FORECAST_HORIZON], series.iloc[-FORECAST_HORIZON:]
        backtest_model = ExponentialSmoothing(train, trend="add", seasonal=None).fit()
        backtest_forecast = backtest_model.forecast(FORECAST_HORIZON)
        mape = float(
            (abs((test.values - backtest_forecast.values) / test.values)).mean() * 100
        )

    full_model = ExponentialSmoothing(series, trend="add", seasonal=None).fit()
    future_forecast = full_model.forecast(FORECAST_HORIZON)

    history_df = pd.DataFrame({
        "Date": series.index.astype(str), "Actual": series.values, "Forecast": None,
    })
    forecast_df = pd.DataFrame({
        "Date": future_forecast.index.astype(str), "Actual": None, "Forecast": future_forecast.values,
    })
    combined = pd.concat([history_df, forecast_df], ignore_index=True)
    combined.to_csv(config.PROCESSED_DIR / "revenue_forecast.csv", index=False)

    title = "Monthly Revenue Forecast"
    if mape is not None:
        title += f" (Backtest MAPE: {mape:.2f}%)"

    visualize.multi_line_chart(
        [
            (series.index, series.values, "Actual Revenue", {"marker": "o"}),
            (future_forecast.index, future_forecast.values, f"Forecast (next {FORECAST_HORIZON} months)",
             {"marker": "o", "linestyle": "--", "color": "tab:red"}),
        ],
        title, "Month", "Revenue", "revenue_forecast.png",
    )

    return {
        "mape": mape,
        "forecast": future_forecast,
        "horizon_months": FORECAST_HORIZON,
        "excluded_partial_month": (
            str(excluded_partial_month.to_period("M")) if excluded_partial_month is not None else None
        ),
    }
