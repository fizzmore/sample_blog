import pandas
from datetime import datetime
import seaborn as sns
from matplotlib import pyplot

sns.set_style("darkgrid")


def load_data():

    # For nominal rate, I only store changes on FOMC annoucement date
    tmp_nominal_df = pandas.read_csv('fed_rate_nominal.csv')
    tmp_nominal_df = tmp_nominal_df.loc[tmp_nominal_df['FEDFUNDS'].diff() != 0, :]

    tmp_mkt_df = pandas.read_csv('sp500_close.csv', usecols=['DATE', 'CLOSE'])
    tmp_mkt_df['DATE'] = tmp_mkt_df['DATE'].map(lambda x: str(datetime.strptime(x, '%m/%d/%Y')).split(' ')[0])
    tmp_mkt_df.sort_values(by='DATE', inplace=True)
    tmp_mkt_df.reset_index(drop=True, inplace=True)
    return (pandas.read_csv('fed_rate_effective.csv'), ), tmp_nominal_df, tmp_mkt_df


def plot_fed_rate(in_df, start_date='2022-01-01'):
    plot_df = in_df.loc[in_df['DATE'] >= start_date, :]

    ax = sns.lineplot(data=plot_df, x="DATE", y="FEDFUNDS", marker='o')
    ax.tick_params(axis='x', rotation=90)
    ax.set(ylabel='Fed Rate [%]')
    pyplot.tight_layout()

    pyplot.savefig('fed_rate.png')


def plot_mkt_fed(mkt_df, fed_df, start_date='2022-01-01'):

    plot_fed_df = fed_df.loc[fed_df['DATE'] >= start_date, :]
    plot_mkt_df = mkt_df.loc[mkt_df['DATE'] >= start_date, :]

    plot_df = plot_mkt_df.set_index('DATE').join(plot_fed_df.set_index('DATE'), how='left')
    plot_df.fillna(method='ffill', inplace=True)
    plot_df.reset_index(inplace=True)


    ax = plot_df.plot(x="DATE", y="CLOSE", legend=False)
    ax2 = ax.twinx()
    plot_df.plot(x="DATE", y="FEDFUNDS", ax=ax2, legend=False, color="r")
    ax.figure.legend(loc='upper center', ncol=2)
    ax.tick_params(axis='x', rotation=90)
    ax.set(ylabel='SP 500 Close')
    ax2.set(ylabel='Fed Nominal Rate [%]')

    pyplot.tight_layout()
    pyplot.savefig('mkt_fed_rate.png')


if __name__ == '__main__':
    fed_effective_rate_df, fed_nominal_rate_df, sp500_df = load_data()

    # plot_fed_rate(fed_effective_rate_df, '2021-01-01')
    plot_mkt_fed(sp500_df, fed_nominal_rate_df, '2022-01-01')