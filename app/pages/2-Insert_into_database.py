import streamlit as st
import mysql.connector

# Configurações da conexão
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  passwd="yourpassword",
  database="yourdatabase"
)