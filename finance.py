import plotly.express as px
import pandas as pd
import streamlit as st


def main():
    data = dataframe()
    data = cleaning(data)
    dashboard(data)


# Initializes the dataframe
def dataframe():
    # while True:
    #     try:
    #         path = input("Please provide the path to finance CSV file: ")
    #         if not path:
    #             df = pd.read_csv("personal_transactions.csv")
    #             return df
    #         df = pd.read_csv(path)
    #         return df

    #     except FileNotFoundError:
    #         print("Incorrect path, try again")

    # Enable this if you don't want to use the input version
    return pd.read_csv("personal_transactions.csv")


def cleaning(df):

    # Removes paycheck as it is not an expense
    df = df[df["Category"] != "Paycheck"]

    # Formats the "Date" column into something more readable, and adds new columns for filtering.
    time = pd.to_datetime(df["Date"])
    df["Date"] = time.dt.date
    df["Year"] = time.dt.year

    return df


def dashboard(df):

    # Initiaties streamlit
    st.set_page_config(layout="wide")
    st.title("Expenses")
    left, right = st.columns(2)

    # Formatting of the dashbaord
    with left:
        sunburst_expander = st.expander("Sunburst graph", True)
        pie_expander = st.expander("Pie Chart", True)

    # Formatting of the dashbaord
    with right:
        bar_expander = st.expander("Bar Chart", True)

        df_expander = st.expander("Dataframe", True)

    # Sidebar
    with st.sidebar:
        cat_feat = st.selectbox(
            "Select Category",
            df.loc[
                :, ~df.columns.isin(["Date", "Description", "Amount", "Year"])
            ].columns,
            index=1,
        )
        date_feat = st.selectbox("Select Year", set(df["Year"]))

        # Dataframe connected to date_feat variable, i.e choosing year.
        df = df.loc[df["Year"] == date_feat]

    # The Sunburst graph
    with sunburst_expander:
        fig = px.sunburst(
            df,
            path=[
                "Category",
                "Description",
            ],
            values="Amount",
            width=600,
            height=600,
            color="Category",
        )
        st.plotly_chart(fig)

    # The bar chart
    with bar_expander:
        histo = px.histogram(
            df,
            x=cat_feat,
            y="Amount",
            width=600,
            height=600,
            color="Category",
            text_auto=True,
            labels={"Amount": "Total Spent"},
        )
        st.plotly_chart(histo)

    # The Pie Chart
    with pie_expander:

        pie_category = px.pie(
            df,
            values=df["Amount"],
            names=cat_feat,
            title="Spending by Category",
            width=600,
            height=600,
            hole=0.3,
        )
        pie_category.update_traces(textposition="inside")
        st.plotly_chart(pie_category, use_container_width=False)

    # The dataframe for a CSV overview
    with df_expander:
        st.dataframe(df)


if __name__ == "__main__":
    main()
