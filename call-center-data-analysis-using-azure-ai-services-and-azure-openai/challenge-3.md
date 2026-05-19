# Challenge 03: Visualize Call Center Insights with Power BI

## Introduction

The transcription and analysis pipeline is running, and your Azure SQL Database is being populated with conversation summaries and sentiment results. In this final challenge, you will bring those insights to life using Power BI. You will configure the prebuilt Power BI report to connect to your Azure SQL Database, publish it to the Power BI Service, create a live dashboard, and then upload additional audio files to see the dashboard refresh with new data in real time.

This is the payoff for all the pipeline work - supervisors will be able to open the dashboard in any browser, filter by sentiment (Positive or Negative), explore conversation summaries, and continuously refresh as new calls are processed.

## Challenge Objectives

- Configure the prebuilt Power BI report to connect to the Azure SQL Database
- Publish the report to the Power BI Service
- Configure the SQL Server connection authentication in the Power BI Service
- Create a live Power BI dashboard by pinning the report
- Upload additional audio files and refresh the dashboard to observe updated analytics

## Prerequisites

Before starting this challenge, ensure you have:
- Completed Challenge 1 (Azure resources provisioned, Output table created)
- Completed Challenge 2 (audio files uploaded, JSON transcripts generated in the output container)
- Power BI Desktop installed on the virtual machine (available at **C:\LabFiles\callcenter-dataanalysis.pbix**)

## Steps to Complete

### Step 1: Configure Power BI Data Source Settings

1. On the virtual machine, open **Power BI Desktop** and open **C:\LabFiles\callcenter-dataanalysis.pbix**. Dismiss any SQL Server connection or Evaluating queries pop-ups that appear.

1. From the top ribbon, go to **Transform data > Data source settings**, select the existing data source, and update the connection to point to your SQL database:

   - **Server:** `sqlserver<inject key="Deployment-id" enableCopy="false"></inject>.database.windows.net`
   - **Database:** `Database-<inject key="Deployment-id" enableCopy="false"></inject>`

1. Edit the credentials to use **Database** authentication with the following values and save:

   - **User name:** `sqluser`
   - **Password:** `password.1!!`

1. Close Data source settings, click **Apply Changes**, then **Refresh** to verify the report loads with data.

   > **Note:** If Power BI Desktop becomes unresponsive at any point, close and reopen it.

### Step 2: Publish the Power BI Report

1. From the top ribbon, click **Publish** and save the report when prompted.

1. Sign in with your lab credentials using **Work or school account**:

   - **Email:** `<inject key="AzureAdUserEmail"></inject>`
   - **Password:** `<inject key="AzureAdUserPassword"></inject>`

   > **Note:** If prompted to stay signed in to all apps, select **No, sign in to this app only**. Dismiss any Power BI license prompts.

1. Select **My workspace**, click **Select**, and once publishing completes, open the report in Power BI Service.

### Step 3: Configure Power BI Service Connection

1. In the Power BI Service, go to **Settings > Manage connections and gateways** from the top-right corner.

1. On the **Data (Preview)** page, select the existing SQL Server connection and open its **Settings**.

1. Configure the connection with the following values and click **Save**, then **Close**:

   - **Authentication Method:** `Basic`
   - **Username:** `sqluser`
   - **Password:** `password.1!!`
   - **Privacy level:** `None`

### Step 4: Create and Explore Power BI Dashboard

1. From the left navigation, go to **My workspace** and open the report named **callcenter-dataanalysis**.

1. On the report page, click the **ellipsis (...)** beside the **Edit** option and select **Pin to dashboard**.

1. Choose **New dashboard**, set the name to **callcenter-dataanalysis**, and click **Pin live**.

1. Click **Go to dashboard** and explore the visualizations. Use the filter checkboxes on the dashboard to filter results by sentiment or conversation file.

### Step 5: Upload Additional Audio Files and Refresh Dashboard

1. In the Azure portal, open the Storage Account **callcenterstore<inject key="Deployment-id" enableCopy="false"></inject>**, navigate to the **audio-input** container, and upload the following two additional audio files from **C:\LabFiles\Recordings**:

   - **Call_health_insurance.wav**
   - **good_review.wav**

1. Wait approximately 5-10 minutes for the files to be processed through the pipeline.

1. Return to your Power BI Dashboard and click **Refresh** to view the updated results with the new calls included.

   > **Note:** The dashboard visualizations update after the transcription and analysis workflow completes for the new files.

<validation step="805aa93b-f620-4d5b-813a-d651daef24a1" />

> **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
> - Navigate to the Lab Validation Page from the upper-right corner in the lab guide section.
> - Click on the **Validate** button for the corresponding task.
> - If you receive a success message, you can proceed to the next task.
> - If validation fails, carefully review the error message and retry the steps by following the instructions in the lab guide.
> - If you need assistance, please contact us at **cloudlabs-support@spektrasystems.com**. We are available 24/7 to help you.

## Success Criteria

- Power BI report is configured with the correct SQL Server and Database values for your deployment
- Report loads successfully with data from the Azure SQL Database
- Report is published to **My workspace** in the Power BI Service
- SQL Server connection is authenticated with Basic credentials in the Power BI Service
- A live dashboard named **callcenter-dataanalysis** is created and shows call center visualizations
- Two additional audio files (Call_health_insurance.wav, good_review.wav) are uploaded and the dashboard refreshes with updated sentiment and summary data

## Additional Resources

- [Get started with Power BI Desktop](https://learn.microsoft.com/power-bi/fundamentals/desktop-getting-started)
- [Publish datasets and reports from Power BI Desktop](https://learn.microsoft.com/power-bi/create-reports/desktop-upload-desktop-files)
- [Create a dashboard from a report in Power BI](https://learn.microsoft.com/power-bi/create-reports/service-dashboard-create)

## Congratulations!

You have successfully built a complete end-to-end call center analytics pipeline using Azure AI Services and Azure OpenAI!

### Real-World Applications:

This solution can transform call center operations across:
- **Customer Sentiment Monitoring:** Automatically flag negative sentiment calls for supervisor review
- **Quality Assurance:** Analyze conversation summaries to ensure agents follow correct procedures
- **Trend Analysis:** Track recurring customer issues across departments over time
- **Performance Reporting:** Give managers real-time dashboards instead of manual call reviews
- **Compliance:** Maintain searchable transcripts of all customer interactions for audit purposes

Click **Next** at the bottom of the page to proceed to the next page.

   ![](./images/GS001.png)
