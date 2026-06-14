"""
==========================================================

QuantEdge AI

Report Generator

Responsibilities
----------------
1. Generate Daily Report
2. Generate Trade Summary
3. Generate Performance Summary

==========================================================
"""

from datetime import datetime


class ReportGenerator:

    @staticmethod
    def daily_report(summary):

        lines = []

        lines.append("=" * 60)
        lines.append("QuantEdge AI Daily Report")
        lines.append("=" * 60)

        lines.append(
            f"Generated : {datetime.now()}"
        )

        lines.append("")

        lines.append(
            f"Total Trades : {summary.total_trades}"
        )

        lines.append(
            f"Winning Trades : {summary.winning_trades}"
        )

        lines.append(
            f"Losing Trades : {summary.losing_trades}"
        )

        lines.append(
            f"Win Rate : {summary.win_rate:.2f}%"
        )

        lines.append(
            f"Gross Profit : {summary.gross_profit:.2f}"
        )

        lines.append(
            f"Gross Loss : {summary.gross_loss:.2f}"
        )

        lines.append(
            f"Net Profit : {summary.net_profit:.2f}"
        )

        lines.append(
            f"Average Profit : {summary.average_profit:.2f}"
        )

        lines.append(
            f"Average Loss : {summary.average_loss:.2f}"
        )

        lines.append(
            f"Profit Factor : {summary.profit_factor:.2f}"
        )

        lines.append(
            f"Max Drawdown : {summary.max_drawdown:.2f}"
        )

        lines.append("=" * 60)

        return "\n".join(lines)

    @staticmethod
    def trade_report(trades):

        report = []

        report.append("=" * 60)
        report.append("Trade Report")
        report.append("=" * 60)

        for i, trade in enumerate(trades, start=1):

            report.append(
                f"{i}. "
                f"{trade['symbol']} | "
                f"{trade['type']} | "
                f"{trade['price']} | "
                f"{trade['quantity']}"
            )

        report.append("=" * 60)

        return "\n".join(report)