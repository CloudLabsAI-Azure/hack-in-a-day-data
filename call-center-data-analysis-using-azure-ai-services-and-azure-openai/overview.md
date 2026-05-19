# Call Center Data Analysis using Azure AI Services and Azure OpenAI - Hack in a Day

Welcome to the Call Center Data Analysis Hack in a Day! In this lab, you will build an end-to-end pipeline that processes real call center recordings, transcribes them using Azure Speech Services, analyzes them with Azure OpenAI, and visualizes the insights through a Power BI dashboard.

## Scenario

Contoso's call center handles thousands of customer interactions every day across departments like health insurance, pharmacy, loans, and general support. Supervisors currently spend hours manually reviewing call recordings to understand customer sentiment and identify recurring issues. Contoso wants to automate this process using Azure AI services to transcribe calls, detect sentiment, summarize conversations, and surface insights through a live Power BI dashboard. The goal is to give supervisors real-time visibility into call quality and customer satisfaction without manual effort.

## Introduction

In this lab, you will set up an Azure-based pipeline that takes raw audio recordings of agent-customer conversations and turns them into actionable business intelligence. Using Azure Functions, Azure Speech Services, Azure OpenAI, Azure SQL Database, and Power BI, you will build a fully automated analysis workflow.

Audio files uploaded to an Azure Storage container automatically trigger a transcription pipeline through Azure Event Grid and Service Bus. Azure Speech Services converts the audio to text, Azure OpenAI analyzes the transcripts for summaries and sentiment, and the results are stored in Azure SQL Database. You then connect Power BI to that database to create a live dashboard that lets supervisors explore call sentiment, filter by outcome, and refresh as new calls are processed.

## Key Tools and Services

In this lab, you will work with:

- **Azure ARM Templates** - For provisioning the complete lab infrastructure in one deployment
- **Azure Storage Account** - For uploading audio files and storing transcript outputs
- **Azure Event Grid and Service Bus** - For coordinating the automated transcription workflow
- **Azure Speech Services** - For batch transcription of audio recordings to text
- **Azure OpenAI** - For generating conversation summaries and performing sentiment analysis
- **Azure Functions** - For orchestrating the transcription and analysis pipeline
- **Azure SQL Database** - For storing analysis results for visualization
- **Power BI Desktop and Power BI Service** - For creating and publishing call center insight dashboards

## Learning Objectives

By the end of this Hack in a Day, you will learn how to:

- Deploy Azure resources at scale using an ARM Template
- Configure an event-driven audio processing pipeline using Azure Functions, Event Grid, and Service Bus
- Use Azure Speech Services batch transcription to convert audio recordings to text
- Leverage Azure OpenAI to extract conversation summaries and perform sentiment analysis
- Store structured AI analysis results in Azure SQL Database
- Connect Power BI to Azure SQL Database and publish reports to Power BI Service
- Create live dashboards and refresh them as new data arrives

## Hack in a Day Format: Challenge-Based

This hack in a day follows a challenge-based format with three stages that build a complete call center analytics solution:

- **Challenge 1: Provision Azure Resources and Configure SQL Database** - Deploy the ARM Template to provision all required Azure services and create the SQL Output table for storing analysis results
- **Challenge 2: Upload Audio Files and Trigger the Transcription Pipeline** - Restart Azure Function Apps, upload call recordings to Azure Storage, and verify that transcripts are generated in the output container
- **Challenge 3: Visualize Call Center Insights with Power BI** - Configure the Power BI report, publish it to Power BI Service, build a live dashboard, and refresh it with additional audio files to see updated analytics

Throughout each challenge, you will:
- Work with real Azure AI services in a provisioned environment
- Trigger and monitor automated event-driven workflows
- Test each stage of the pipeline end-to-end
- End up with a live Power BI dashboard showing call sentiment and conversation summaries

## Challenge Overview

You start by deploying an ARM Template that provisions the full Azure infrastructure including Storage Account, Service Bus, Event Grid, Key Vault, Speech Service, Azure OpenAI, three Azure Function Apps, and Azure SQL Database. You then create the Output table in the SQL Database that will store the AI-generated analysis results.

Next, you restart the Azure Function Apps to ensure all services are running, upload three sample call recordings to the Azure Storage audio-input container, and verify that the automated pipeline converts them into JSON transcript files stored in the output container.

Finally, you open a prebuilt Power BI report, configure it to connect to your Azure SQL Database, publish it to Power BI Service, and pin it to a live dashboard. You upload two more audio files, refresh the dashboard, and explore sentiment analysis and conversation summaries across all processed calls.

## Support Contact

The CloudLabs support team is available 24/7, 365 days a year, via email and live chat to ensure seamless assistance at any time.

Learner Support Contacts:

- Email Support: cloudlabs-support@spektrasystems.com
- Live Chat Support: https://cloudlabs.ai/labs-support

Click **Next** at the bottom of the page to proceed to the next page.

   ![](./images/auto-it-gt-gr-g2.png)

## Happy Hacking!!
