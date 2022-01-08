from pathlib import Path
import pandas as pd
from engineer import sql_writer as sqw


def check_incoming(f):
	if 'GoogleEarningsReport' in f.stem and f.suffix == '.csv':
		return True


def get_df(f):
	df = pd.DataFrame()
	try:
		df = pd.read_csv(f, encoding='utf-16', sep='\t', header=0, index_col=None)
	except Exception as e:
		print(f"mar konvertaltuk..., error: {e}")
		df = pd.read_csv(f, sep='\t', header=0, index_col=None)
	finally:
		return df


def google_audio(finrep_dir, table='stg_fin2_20012_google_audio', hova='19'):
	files = []
	src = Path(finrep_dir).joinpath('google_audio')
	for f in src.iterdir():
		if check_incoming(f):
			files.append(f)
	for f in files:
		df = get_df(f)
		print(f.name, df['Earnings Amount'].astype(float).sum())

	if len(files) > 1:
		period_file = {}
		for f in files:
			name_parts = f.stem.split('_')
			period = tuple(name_parts[-1].split('-'))
			period_file[period[0] * 100 + period[1]] = f
		the_one = period_file[sorted(period_file.keys())[-1]]
		df = get_df(the_one)
	else:
		df = files[0]
	print(df.info)
	sqw.write_to_db(df, table, action='replace', hova=hova)


if __name__ == '__main__':
	google_audio('/Users/frank/pd/finance_report', hova='19')
	# google_audio('h:/NextCloud/Finance/szamitas/2021_11_november')
