import calendar
import matplotlib.pyplot as plt
import pandas as pd

def plot_allocations_over_time(allocations_over_time):
    """
    Creates a plot to show the allocations given to each alpha over time.
    
    Input:
     - allocations_over_time
        A DataFrame which lists how much to allocate to each alpha over time
    """
    f, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(16, 10))
    
    # Calculate bar plot widths
    widths = []
    for time, row in allocations_over_time.iterrows():
        days_in_month = calendar.monthrange(time.year, time.month)[1]
        widths.append(days_in_month - time.day - 0.5)
    
    # Stacked bar plot
    ax1.set_title('Alpha Allocations Over Time')
    ax1.set_ylabel('Portfolio Weight (%)')
    x = allocations_over_time.index 
    previous_allocations = [0] * allocations_over_time.shape[0]
    for alpha in allocations_over_time.columns:
        current_allocations = allocations_over_time[alpha].fillna(0) * 100
        ax1.bar(x, current_allocations, widths, bottom=previous_allocations, align='edge', label=alpha)
        previous_allocations = current_allocations + previous_allocations
    ax1.legend(allocations_over_time.columns, frameon=True, framealpha=0.7, facecolor='white')
    
    # Bar plot
    number_of_alphas_allocated_to = []
    for time, row in allocations_over_time.iterrows():
        number_of_alphas_allocated_to.append(len(row[row > 0]))
    ax2.bar(x, number_of_alphas_allocated_to, width=widths, align='edge')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Number of Alphas Allocated To')
    plt.xticks(rotation=-90)
    y_ticks = range(0, max(number_of_alphas_allocated_to)+1)
    ax2.yaxis.set_ticks(y_ticks)
    ax2.margins(0)
    plt.show()
    
def plot_all_equity_curves(equity_curves, composite_equity_curve):
    """
    Plot the equity curves and composite equity curve in a single line chart.
    
    Input:
     - equity_curves
        Equity curves of the alphas
     - composite_equity_curve
        Equity curve of the optimized portfolio
    """
    all_curves = pd.DataFrame()
    all_curves = equity_curves.join(composite_equity_curve, how = 'outer')
    all_curves[equity_curves.columns].plot(figsize=(16, 6), c='grey')
    all_curves['*CompositeAlpha*'].plot(c='orange', linewidth=4)
    plt.legend(all_curves.columns)
    plt.title('Alpha Equity vs Optimized Portfolio Equity')
    plt.xlabel('Date')
    plt.ylabel('Normalized Equity')
    plt.show()
