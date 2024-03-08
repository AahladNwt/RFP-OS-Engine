def page_style(outputs):
    
    page_top = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Global styles for the entire page */
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }

            /* Style the header */
            .header {
                background-color: #4CAF50;
                color: #fff;
                padding: 20px;
                text-align: center;
            }

            /* Style the header text */
            .header h1 {
                font-size: 36px;
            }

            /* Style the main content area */
            .content {
                padding: 20px;
            }

            /* Style the footer */
            .footer {
                background-color: #4CAF50;
                color: #fff;
                padding: 10px;
                text-align: center;
            }

            .page-break {
                page-break-before: always;
            }
        
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <h1>Technical Proposal</h1>
        </div>

        <!-- Main Content -->
        <div class="content">
        """

    page_bottom = """ </div>

        <!-- Footer -->
        <div class="footer">
            &copy; 2023 NewWave
        </div>
    </body>
    </html>

    """
    final_output = page_top + outputs + page_bottom
    
    return final_output

section_title = """ </div>
        <!-- Header -->
        <div class="header">
            <h1> {} </h1>
        </div>

        <!-- Main Content -->
        <div class="content">
        
        """

table_css = """
.my-table-class {
    font-family: Arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

.my-table-class td, th {
    border: 1px solid #ddd;
    padding: 8px;
}

.my-table-class tr:nth-child(even) {
    background-color: #f2f2f2;
}

.my-table-class th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}
"""

def page_style(outputs):
    
    page_top = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Global styles for the entire page */
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                margin: 0;
                padding: 0;
            }

            /* Style the header */
            .header {
                background-color: #4CAF50;
                color: #fff;
                padding: 20px;
                text-align: center;
            }

            /* Style the header text */
            .header h1 {
                font-size: 36px;
            }

            /* Style the main content area */
            .content {
                padding: 20px;
            }

            /* Style the footer */
            .footer {
                background-color: #4CAF50;
                color: #fff;
                padding: 10px;
                text-align: center;
            }

            .page-break {
                page-break-before: always;
            }
        
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <h1>Technical Proposal</h1>
        </div>

        <!-- Main Content -->
        <div class="content">
        """

    page_bottom = """ </div>

        <!-- Footer -->
        <div class="footer">
            &copy; 2023 NewWave
        </div>
    </body>
    </html>

    """
    final_output = page_top + outputs + page_bottom
    
    return final_output

table_css = """
.my-table-class {
    font-family: Arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

.my-table-class td, th {
    border: 1px solid #ddd;
    padding: 8px;
}

.my-table-class tr:nth-child(even) {
    background-color: #f2f2f2;
}

.my-table-class th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #4CAF50;
    color: white;
}
"""