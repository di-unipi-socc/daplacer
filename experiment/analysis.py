import pandas as pd
import matplotlib.pyplot as plt


def main():
	df = pd.read_csv("csv/results2.csv")

	A = "Exh"
	field = "Inferences"
	col_name = "Infs"

	rates = df["Rate"].unique()
	sizes = df['Size'].unique()
	x = [i for i in range(len(sizes))]

	plt.figure()
	plt.xticks(x, sizes)
	plt.xlabel("Infrastructure Size")
	plt.ylabel(field)
	plt.title("{} - {}".format(A, field))
	for r in rates:
		y = df.loc[df["Rate"] == r][col_name]
		lbl = str(r*100) + "%"
		plt.plot(x, y, marker='o', label=lbl)
	plt.legend(loc="upper left")

	axes = plt.gca()
	axes.set_ylim([60000, 490000])
	# axes.set_ylim([0, .12])
	plt.savefig("csv/{}_{}.png".format(A.lower(), col_name.lower()), dpi=600)
	plt.show()


if __name__ == '__main__':
	main()
