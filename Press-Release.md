# Rising Rakers and Aging Sluggers: Data-Driven Analysis of Top Breakout and Regression Candidates for the 2026 MLB Campaign (NL Edition)

## Hook

Which hitters are about to take the next leap, and which veterans may finally begin to lose their edge? By analyzing decades of MLB batting data and advanced sabermetrics, this project uses machine learning to identify National League players most likely to experience breakout seasons or performance regression in 2026, turning historical trends into forward-looking insights.

## Problem Statement

Projecting player performance is one of the most difficult and important challenges in baseball analysis. Teams, analysts, and fans regularly try to identify which young hitters are poised for breakout seasons and which aging veterans may begin to decline, but these judgments are often based on intuition, small sample observations, or isolated statistics rather than systematic analysis. While modern baseball analytics provides a wide range of advanced metrics that capture different aspects of player performance, it is not always clear which of these indicators meaningfully signal future improvement or decline.

This project addresses that challenge by analyzing historical MLB data to determine whether advanced batting statistics from one season can help predict significant changes in offensive performance in the following season. Specifically, the project focuses on two age groups in the National League: players aged 20–25, who are candidates for breakout seasons, and players aged 30–35, who may be more likely to experience regression. Using a relational database and a machine learning pipeline, the project aims to identify which statistical patterns precede large increases or decreases in offensive production, and to apply those insights to generate predictions for the 2026 MLB season.

## Solution Description

To address this problem, the project analyzes decades of historical MLB data to identify patterns that tend to precede major changes in offensive performance. Using publicly available statistics from FanGraphs, the dataset was constructed with season-level information for National League hitters within two key age groups: players aged 20–25, who are often entering their physical prime and may be poised for breakout seasons, and players aged 30–35, who are more likely to experience performance decline. The data includes both traditional batting statistics (such as batting average, on-base percentage, and slugging percentage) and advanced sabermetric indicators that capture plate discipline, power, and overall offensive value.

To determine what constitutes a true breakout or regression, the project examined year-over-year changes in OPS (on-base plus slugging percentage) across historical seasons. Instead of relying on arbitrary thresholds, breakout seasons were defined as those falling in the top 25% of OPS increases, while regression seasons were defined as those falling in the bottom 25% of OPS changes. These thresholds allowed the analysis to focus on the most meaningful performance shifts observed in real MLB data.

A machine learning model was then trained on historical seasons to learn which advanced statistics from one year tend to precede these large increases or decreases in offensive production the following year. After evaluating the model using cross-validation to ensure reliable performance, the trained models were applied to the most recent available season of data to generate predictions for the 2026 MLB season. The result is a data-driven framework that highlights the National League hitters most likely to break out or regress, along with the statistical factors that contributed most strongly to those predictions.

## Chart

Visualization 1 (Breakout): https://drive.google.com/file/d/1AEDkg9M1DtscFPagNZsuDnzwyzset8Hl/view?usp=sharing

Visualization 2 (Regression): https://drive.google.com/file/d/1rBbAuTZ2iwX4rdUOLHpsqK4Ks9fF5-Da/view?usp=sharing
