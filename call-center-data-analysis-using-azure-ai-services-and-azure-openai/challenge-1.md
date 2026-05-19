# Challenge 01: Provision Azure Resources and Configure SQL Database

## Introduction

Before any audio can be processed, the full Azure infrastructure needs to be in place. This challenge focuses on deploying the complete set of Azure services required for the call center analytics pipeline using an ARM Template. Once the infrastructure is provisioned, you will also prepare the Azure SQL Database by creating the Output table that will store the AI-generated conversation summaries and sentiment analysis results.

## Challenge Objectives

- Deploy the ARM Template to provision all required Azure resources for the call center pipeline
- Create the Output table in Azure SQL Database to store analysis results

## Prerequisites

Before starting this challenge, ensure you have:
- Signed in to the Azure portal using the lab credentials
- Access to the lab files at **C:\LabFiles** on the virtual machine

## Steps to Complete

### Step 1: Deploy Azure Resources using ARM Template

1. In the Azure portal, search for **Deploy a custom template** and open it.

1. Select **Build your own template in the editor**, use **Load file** to load **azuredeploy-01.json** from **C:\LabFiles**, and click **Save**.

1. On the **Custom deployment** page, configure the following and leave all other values at their defaults:

   - **Resource group:** `callcenter-<inject key="Deployment-id" enableCopy="false"></inject>`
   - **Deployment Id Parameter:** `<inject key="Deployment-id" enableCopy="false"></inject>`

1. Click **Review + create**, then **Create**. Wait for the deployment to complete (~6-7 minutes) before proceeding.

   > **Note:** Do not proceed until the deployment completes successfully.

<validation step="9a272f75-49e1-4afc-92b2-42e223893d0b" />

> **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
> - Navigate to the Lab Validation Page from the upper-right corner in the lab guide section.
> - Click on the **Validate** button for the corresponding task.
> - If you receive a success message, you can proceed to the next task.
> - If validation fails, carefully review the error message and retry the steps by following the instructions in the lab guide.
> - If you need assistance, please contact us at **cloudlabs-support@spektrasystems.com**. We are available 24/7 to help you.

### Step 2: Create Output Table in Azure SQL Database

1. In the Azure portal, open **Database-<inject key="Deployment-id" enableCopy="false"></inject>** and go to **Query editor (Preview)**. Sign in with the following credentials:

   - **Login:** `sqluser`
   - **Password:** `password.1!!`

1. Run the following SQL script to create the Output table:

   ```sql
   CREATE TABLE dbo.Output (
       ID NVARCHAR(255) NOT NULL PRIMARY KEY,
       FileName NVARCHAR(MAX) NULL,
       Sentiment NVARCHAR(MAX) NULL,
       Summary NVARCHAR(MAX) NULL
   );
   ```

1. Confirm the table exists by running the following query and verifying the `Output` table appears in the results:

   ```sql
   SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Output';
   ```

## Success Criteria

- ARM Template deployment completes successfully with all Azure resources provisioned in the **callcenter-<inject key="Deployment-id" enableCopy="false"></inject>** resource group
- The `Output` table is created in **Database-<inject key="Deployment-id" enableCopy="false"></inject>** and verified through the Query Editor

## Additional Resources

- [Deploy resources with ARM templates](https://learn.microsoft.com/azure/azure-resource-manager/templates/deploy-portal)
- [Quickstart: Use the Azure portal Query editor to query Azure SQL Database](https://learn.microsoft.com/azure/azure-sql/database/connect-query-portal)

Click **Next** at the bottom of the page to proceed to the next page.

   ![](./images/GS001.png)
