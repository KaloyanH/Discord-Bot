import discord
import matplotlib.pyplot as plt
from io import BytesIO


async def visualize_table(channel, df):
    plt.figure(figsize=(12, 8))

    df.sort_values(by='Price', inplace=True, ascending=False)

    bar_width = 0.6

    bars = plt.barh(df['Product Name'], df['Price'], color='skyblue', height=bar_width)
    plt.ylabel('Product Name')
    plt.title('Product Prices')
    plt.tight_layout()

    for index, bar in enumerate(bars):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, df['Price'][index],
                 ha='left', va='center', rotation=0)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await channel.send(file=discord.File(buffer, filename='product_chart.png'))

    plt.close()
