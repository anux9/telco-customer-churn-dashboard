import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# إعداد الصفحة
st.set_page_config(
    page_title="Telco Customer Churn Dashboard",
    layout="wide" )

# قراءة البيانات
df = pd.read_csv("telco_model_ready.csv")

# عنوان التطبيق
st.title("Telco Customer Churn Dashboard")
st.write("Analysis of customer churn and the factors affecting it.")


# إضافة الفلاتر في الشريط الجانبي
st.sidebar.header("Filters")

contract_filter = st.sidebar.multiselect(
    "Contract Type",
    df['Contract'].unique(),
    default=df['Contract'].unique()
)

internet_filter = st.sidebar.multiselect(
    "Internet Service",
    df['InternetService'].unique(),
    default=df['InternetService'].unique()
)

tenure_filter = st.sidebar.multiselect(
    "Tenure Group",
    df['Tenure_Group'].unique(),
    default=df['Tenure_Group'].unique() )

# تطبيق الفلاتر على البيانات
filtered_df = df[
    (df['Contract'].isin(contract_filter)) &
    (df['InternetService'].isin(internet_filter)) &
    (df['Tenure_Group'].isin(tenure_filter)) ]

# حساب الأرقام الرئيسية
total_customers = len(filtered_df)
churned_customers = len(filtered_df[filtered_df['Churn'] == 1])
churn_rate = (churned_customers / total_customers * 100) if total_customers > 0 else 0
active_customers = total_customers - churned_customers

# عرض الأرقام الرئيسية
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", total_customers)
col2.metric("Churned Customers", churned_customers)
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Active Customers", active_customers)

# الرسم الأول: العلاقة بين نوع العقد ومغادرة العملاء
st.subheader("Churn by Contract")

fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='Contract', hue='Churn', ax=ax)
st.pyplot(fig)

# الرسم الثاني: العلاقة بين مدة اشتراك العميل ومغادرته
st.subheader("Churn by Tenure Group")

fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x='Tenure_Group', hue='Churn', ax=ax)
st.pyplot(fig)

# أهم 3 نتائج من التحليل
st.subheader("Top 3 Findings")

st.write("1. Around 26.58% of customers left the company.")

st.write("2. New customers had the highest number of churn cases, with 1,037 customers leaving.")

st.write("3. The High charges category had the highest churn rate at 37.85%.")