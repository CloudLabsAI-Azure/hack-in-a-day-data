# Challenge 02: Upload Audio Files and Trigger the Transcription Pipeline

## Introduction

With the Azure infrastructure in place, it is time to feed the pipeline with real call center recordings. In this challenge, you will prepare the Azure Function Apps for processing, upload sample agent-customer audio files to Azure Storage, and verify that the automated transcription pipeline picks them up and generates JSON transcript files.

When an audio file lands in the **audio-input** container, Azure Event Grid detects the blob creation event and routes it through the Service Bus queue. The **StartTranscription** Function App picks it up and initiates a batch transcription job using Azure Speech Services. Once transcription completes, the **FetchTranscription** Function App places the resulting JSON transcript into the **json-result-output** container, where the **AnalyzeTranscription** Function App then takes over to produce summaries and sentiment using Azure OpenAI.

## Challenge Objectives

- Restart Azure Function Apps to ensure all services are running correctly
- Upload call recording audio files to the Azure Storage audio-input container
- Verify that the transcription pipeline generates JSON transcript files in the output container

## Prerequisites

Before starting this challenge, ensure you have:
- Completed Challenge 1 (all Azure resources deployed, Output table created)
- Access to audio files at **C:\LabFiles\Recordings** on the virtual machine

## Steps to Complete

### Step 1: Restart Azure Function Apps

1. In the Azure portal, search for **Function App** and open the Function Apps listing.

1. Select all three Function Apps and click **Restart** from the top menu. Confirm the restart when prompted.

   > **Note:** Wait until all three Function Apps show a **Running** state before proceeding.

### Step 2: Upload Audio Files to Azure Storage Account

1. In the Azure portal, open Storage Account **callcenterstore<inject key="Deployment-id" enableCopy="false"></inject>**, navigate to **Containers > audio-input**, and upload the following files from **C:\LabFiles\Recordings**:

   - **bad_review.wav**
   - **Call__pharmacy_call.wav**
   - **Call_apply_loan.wav**

   > **Note:** Once uploaded, the transcription workflow starts automatically through Azure Functions, Event Grid, and Service Bus.

### Step 3: Verify JSON Transcript Output

1. Wait approximately 5-10 minutes, then open the **json-result-output** container on the same Storage Account.

1. Verify that JSON transcript files have been generated for each of the three uploaded audio files.

   > **Note:** These JSON files contain the raw transcription data. The AnalyzeTranscription Function App will process them using Azure OpenAI to produce summaries and sentiment results, which are then loaded into Azure SQL Database.

<validation step="1a402466-f176-4f15-baac-579c72808eb5" />

> **Congratulations** on completing the task! Now, it's time to validate it. Here are the steps:
> - Navigate to the Lab Validation Page from the upper-right corner in the lab guide section.
> - Click on the **Validate** button for the corresponding task.
> - If you receive a success message, you can proceed to the next task.
> - If validation fails, carefully review the error message and retry the steps by following the instructions in the lab guide.
> - If you need assistance, please contact us at **cloudlabs-support@spektrasystems.com**. We are available 24/7 to help you.

## Success Criteria

- All three Azure Function Apps are in the **Running** state
- Three audio files (bad_review.wav, Call__pharmacy_call.wav, Call_apply_loan.wav) are uploaded to the **audio-input** container
- Corresponding JSON transcript files appear in the **json-result-output** container after the transcription pipeline completes

## Additional Resources

- [Azure Event Grid overview](https://learn.microsoft.com/azure/event-grid/overview)
- [What is Azure Service Bus?](https://learn.microsoft.com/azure/service-bus-messaging/service-bus-messaging-overview)
- [What is the Speech service?](https://learn.microsoft.com/azure/ai-services/speech-service/overview)

Click **Next** at the bottom of the page to proceed to the next page.

   ![](./images/GS001.png)
