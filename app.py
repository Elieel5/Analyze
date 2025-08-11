import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

st.set_page_config(page_title="Análise de Vendas", layout="wide")
sns.set_style("whitegrid")

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.3


@st.cache_data
def carregar_dados(arquivo_csv):
    df = pd.read_csv(arquivo_csv)
    df["Data"] = pd.to_datetime(df["Data"])
    df["Mes"] = df["Data"].dt.to_period("M")
    df["Ano"] = df["Data"].dt.year
    df["Mes_Numero"] = df["Data"].dt.month
    df["Dia_da_Semana"] = df["Data"].dt.day_name(locale="pt_BR")
    return df


@st.cache_data
def calcular_metricas(df):
    vendas_mensais = df.groupby("Mes")["Venda_Total"].sum().reset_index()
    vendas_mensais["Mes_str"] = vendas_mensais["Mes"].astype(str)
    vendas_mensais["Crescimento_Percentual"] = (
        vendas_mensais["Venda_Total"].pct_change() * 100
    )

    total = df["Venda_Total"].sum()
    media = vendas_mensais["Venda_Total"].mean()
    crescimento_total = 0
    if len(vendas_mensais) > 1:
        crescimento_total = (
            (
                vendas_mensais["Venda_Total"].iloc[-1]
                / vendas_mensais["Venda_Total"].iloc[0]
            )
            - 1
        ) * 100

    return total, media, crescimento_total, vendas_mensais


def download_plot_button(fig, filename, label):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    st.download_button(
        label=label, data=buf.getvalue(), file_name=filename, mime="image/png"
    )


def plot_vendas_mensais(vendas_mensais):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        vendas_mensais["Mes_str"],
        vendas_mensais["Venda_Total"],
        marker="o",
        color="blue",
    )
    ax.set_title("Evolução das Vendas Mensais", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Total Vendido (R$)")
    ax.tick_params(axis="x", rotation=45)
    ax.ticklabel_format(style="plain", axis="y")
    st.pyplot(fig)
    download_plot_button(
        fig, "grafico_vendas_mensais.png", "📤 Baixar Gráfico de Vendas Mensais"
    )


def plot_crescimento_percentual(vendas_mensais):
    fig, ax = plt.subplots(figsize=(12, 5))
    crescimento = vendas_mensais["Crescimento_Percentual"].dropna()
    meses = vendas_mensais["Mes_str"].iloc[1:]
    cores = ["green" if x >= 0 else "red" for x in crescimento]
    ax.bar(meses, crescimento, color=cores, alpha=0.8)
    ax.set_title(
        "Crescimento Percentual Mensal", fontsize=14, fontweight="bold")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Crescimento (%)")
    ax.axhline(y=0, color="black", linestyle="--", alpha=0.5)
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig)
    download_plot_button(
        fig,
        "grafico_crescimento_percentual.png",
        "📤 Baixar Gráfico de Crescimento Percentual",
    )


def plot_grafico_combinado(vendas_mensais):
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Gráfico de barras - Vendas
    ax1.bar(
        vendas_mensais["Mes_str"],
        vendas_mensais["Venda_Total"],
        color="skyblue",
        alpha=0.7,
        label="Vendas (R$)",
    )
    ax1.set_xlabel("Mês")
    ax1.set_ylabel("Vendas Totais (R$)", color="blue")
    ax1.tick_params(axis="x", rotation=45)

    # Segundo eixo - Crescimento
    ax2 = ax1.twinx()
    ax2.plot(
        vendas_mensais["Mes_str"],
        vendas_mensais["Crescimento_Percentual"],
        color="orange",
        marker="o",
        linewidth=2,
        label="Crescimento (%)",
    )
    ax2.set_ylabel("Crescimento (%)", color="orange")

    # Título e legendas
    fig.suptitle(
        "Vendas Mensais e Crescimento Percentual",
        fontsize=14, fontweight="bold"
    )
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    st.pyplot(fig)
    download_plot_button(fig,
                         "grafico_combinado.png", "📤 Baixar Gráfico Combinado")


def main():
    st.title("📊 Dashboard: Análise de Crescimento de Vendas")
    arquivo = st.file_uploader("Upload do arquivo CSV", type=["csv"])

    if arquivo:
        try:
            df = carregar_dados(arquivo)
            st.success(f"{len(df)} registros carregados com sucesso!")

            produtos = df["Produto"].unique().tolist()
            selecionados = st.sidebar.multiselect(
                "Filtrar por Produto:", produtos, default=produtos
            )
            df = df[df["Produto"].isin(selecionados)]

            data_min, data_max = df["Data"].min(), df["Data"].max()
            inicio = st.sidebar.date_input("Data Inicial", data_min)
            fim = st.sidebar.date_input("Data Final", data_max)
            df = df[
                (df["Data"] >= pd.to_datetime(inicio))
                & (df["Data"] <= pd.to_datetime(fim))
            ]

            st.dataframe(df.head())

            (
                total,
                media,
                crescimento_total,
                vendas_mensais, ) = calcular_metricas(df)

            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Vendido", f"R$ {total:,.2f}")
            col2.metric("📈 Média Mensal", f"R$ {media:,.2f}")
            col3.metric("🚀 Crescimento Total", f"{crescimento_total:.2f}%")

            plot_vendas_mensais(vendas_mensais)
            plot_crescimento_percentual(vendas_mensais)
            plot_grafico_combinado(vendas_mensais)

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")


if __name__ == "__main__":
    main()
