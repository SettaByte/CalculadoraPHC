# Overview

This is a Streamlit-based cutting calculator application for optimizing paper cuts. The application helps users calculate the most efficient way to cut smaller pieces from larger paper sheets, considering both normal and rotated orientations to maximize material utilization. It features a pink pastel theme and includes capabilities for saving calculations, exporting reports, and managing predefined templates.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web framework for rapid UI development
- **Styling**: Custom CSS with pink pastel theme using CSS variables for consistent design
- **JavaScript**: Custom client-side functionality for interactive elements like floating bars and scroll effects
- **Layout**: Wide layout with collapsible sidebar for optimal screen utilization

## Backend Architecture
- **Main Application**: Single-file Streamlit app (`app.py`) serving as the entry point
- **Modular Design**: Utility modules organized in `utils/` directory:
  - `calculator.py`: Core cutting optimization algorithms
  - `database.py`: Database operations and connection management
  - `export_utils.py`: Report generation in multiple formats
- **Session Management**: Streamlit session state for maintaining calculator instances and user preferences

## Core Calculation Engine
- **Optimization Strategy**: Dual-orientation calculation comparing normal vs rotated cuts
- **Algorithm**: Grid-based cutting calculation with waste minimization
- **Features**: Support for inline cuts (no rotation) and optimal cuts (with rotation consideration)

## Data Storage
- **Database**: PostgreSQL with psycopg2 adapter
- **Connection Handling**: Environment variable-based configuration with fallback options
- **Schema**: Tables for templates, favorite configurations, and calculation history
- **Data Types**: Support for decimal precision measurements and timestamps

## Export System
- **Multiple Formats**: Excel (XLSX) and PDF report generation
- **Libraries**: 
  - `xlsxwriter` for Excel exports with custom formatting
  - `reportlab` for PDF generation with professional styling
  - `pandas` for data manipulation and structuring

## State Management
- **Session Persistence**: Calculator instances, export utilities, and database connections maintained in session state
- **Special Features**: Comparison mode for evaluating multiple cutting configurations
- **User Preferences**: Stored comparison configurations and special code verification

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charting and visualization (Graph Objects and Express)

## Database Integration
- **PostgreSQL**: Primary database system
- **psycopg2**: PostgreSQL adapter for Python with connection pooling

## Export and Reporting
- **xlsxwriter**: Excel file generation with advanced formatting
- **reportlab**: PDF document creation with professional layouts
- **BytesIO**: In-memory file handling for downloads

## UI Enhancement
- **Google Fonts**: Inter font family for typography
- **Font Awesome**: Icon library for enhanced visual elements

## Environment Configuration
- **Environment Variables**: Database connection parameters (DATABASE_URL, PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD)
- **Static Assets**: CSS and JavaScript files for custom styling and interactions