import matplotlib
matplotlib.use("Agg")  # Headless-Backend
import matplotlib.pyplot as plt

# Beispielplot
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Test Plot")
plt.savefig("test_plot.png")
print("Plot wurde mit Agg-Backend als 'test_plot.png' gespeichert.")
