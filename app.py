import streamlit as st
import subprocess
import sys

st.title("Hello Akash")
# Add to sidebar

st.write(
'''
Part 1: Fundamentals (30 min)
Chapter 1: Setup & Core Concepts

Installation & first app
Execution model (top-to-bottom, reruns)
Basic widgets & display elements

Chapter 2: Layouts & Organization

Columns, tabs, expanders, containers
Building structured UIs


Part 2: Data & Interactivity (45 min)
Chapter 3: Working with Data

File uploads & processing
DataFrames display & manipulation
Basic filtering and searching

Chapter 4: Session State (Critical!)

Understanding session state
Persisting data across reruns
Callbacks and state management

Chapter 5: Data Visualization

Built-in charts
Plotly basics
Interactive plots


Part 3: Multi-Page & Navigation (30 min)
Chapter 6: Multi-Page Architecture

Creating separate page files
Page navigation
Sharing data between pages

Chapter 7: Custom Navigation & Routing

Building custom navbars
Dynamic page routing
URL parameters


Part 4: Authentication & Access Control (30 min) 🆕
Chapter 8: User Authentication

Simple login system
Password hashing
Session-based authentication
Logout functionality

Chapter 9: Role-Based Access Control (RBAC)

User roles (Admin, User, Viewer)
Page-level permissions
Feature-level permissions
Protecting routes and content

Chapter 10: Advanced Security

Storing user credentials securely
Database integration for users
Token-based authentication
Best practices


Part 5: Advanced Essentials (30 min)
Chapter 11: Forms & Validation

Creating forms
Input validation
Multi-step workflows

Chapter 12: Caching & Performance

@st.cache_data and @st.cache_resource
Performance optimization


Part 6: Real-World (15 min)
Chapter 13: Database & API Integration

Database connections
API calls
Real-time data

Chapter 14: Deployment & Final Project

Deployment basics
Secrets management
Complete app walkthrough
'''
)