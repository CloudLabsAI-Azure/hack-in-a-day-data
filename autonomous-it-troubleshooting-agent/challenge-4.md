# Challenge 04: Create Topics Using Generative AI

## Introduction
Instead of manually building conversation flows from scratch, Microsoft Copilot Studio allows you to create topics using generative AI. Simply describe what you want the topic to do, and AI will generate the conversation flow, trigger phrases, and responses automatically. You'll then connect these topics to your Freshdesk flow for ticket escalation.

In this challenge, you will create 3 essential IT support topics using generative AI: CredentialResetSupport, VPNConnectivitySupport, and HardwareSupportAssistant. Each topic will call your published Freshdesk flow when escalation is needed.

## Challenge Objectives
- Use Copilot Studio's generative AI to create 3 topics
- Review All Topics
- Connect Topics to Freshdesk Flow

## Steps to Complete

### Step 1: Navigate to Topics Section

1. In your **IT Support Copilot**, click **Topics** in the navigation pane.

1. You'll see existing system topics (Conversation Start, Fallback, Error).

1. Click **+ Add a topic**.

1. Select **Add from description with Copilot**.

### Step 2: Create Topic 1 - CredentialResetSupport

1. In the topic creation dialog, enter the following details:

   - **Name:** `CredentialResetSupport`
   - **Description:**

      ```
      Help users who need password reset assistance when they forget their password or their account becomes locked. Ask the user for their username and save it as a variable. Use generative answers to provide self-service reset instructions by referring to the uploaded knowledge sources whenever possible. After sharing the steps, ask the user whether they were able to reset their password successfully. If not, offer to create a support ticket. When creating the ticket, generate a subject line such as "Password Reset Assistance – <username>" and create a detailed description that includes the username and the reason they were unable to reset the password. Map these values to the Freshdesk Power Automate flow inputs for Subject and Description so the flow receives the correct variables. This topic should act as a guided password-reset helper that uses the knowledge base first, and escalates to ticket creation only when needed.
      ```

1. Click on **Create**.

1. Wait for the AI to generate the topic (15-30 seconds).

1. Review the generated topic:

   - **Trigger phrases:** Verify it includes phrases like:
   - "I forgot my password"
   - "Reset my password"
   - "Account locked"
   - "Can't log in"
   - "Password reset"

1. Review the conversation flow:

1. **Important:** If you see an error about limited scope or variables:
   - Open the **Variables** pane.
   - Click on each variable under **Topic**.
   - Enable the both the checkbox for **Receive values from other topics** or **Return values to original topics** for Variables which shows error.

1. Click **Save** to keep this topic.

<validation step="40ad233d-94ef-47d9-93c7-9232dca6bdc2" />
 
> **Congratulations** on completing the Challenge! Now, it's time to validate it. Here are the steps:
> - Hit the Validate button for the corresponding Challenge. If you receive a success message, you can proceed to the next Challenge. 
> - If not, carefully read the error message and retry the step, following the instructions in the lab guide.
> - If you need any assistance, please contact us at cloudlabs-support@spektrasystems.com. We are available 24/7 to help.

### Step 3: Create Topic 2 - VPNConnectivitySupport

1. Click **+ Add a topic**.

1. Select **Add from description with Copilot**.

1. Enter the following details:

   - **Name:** `VPNConnectivitySupport`
   - **Description:**

      ```
      Assist users experiencing VPN or general internet connectivity issues. Ask the user what exact problem or error message they are seeing and save that response as a variable. Ask where the user is working from, such as home, office, or another location, and save that as another variable. Provide basic troubleshooting steps including checking internet connection, verifying Wi-Fi status, restarting the VPN client, checking login credentials, reconnecting to the network, and any other basic connectivity checks. After giving these steps, ask the user whether the issue is resolved. If the user says no, offer to create a support ticket. When creating the ticket, generate a subject line using the location variable, for example "Connectivity Issue – <location>," and generate a detailed description that includes the user's reported error message and the location information. Map these values to the Freshdesk Power Automate flow inputs for Subject and Description so the flow receives the correct variables. This topic should handle all VPN and internet issues but exclude hardware problems, as those are handled in another topic.
      ```

1. Click **Create** or **Generate**.

1. Review and customize the generated topic:

   - **Trigger phrases:** Verify it includes phrases like:
   - "VPN not connecting"
   - "VPN authentication failed"
   - "Can't connect to VPN"
   - "Internet not working"
   - "Connectivity issues"
   - "Network problems"

1. Review the conversation flow:

1. **Important:** If you see an error about limited scope or variables:
   - Open the **Variables** pane.
   - Click on each variable under **Topic**.
   - Enable the both the checkbox for **Receive values from other topics** or **Return values to original topics** for Variables which shows error.

1. Click **Save**.

### Step 4: Create Topic 3 - HardwareSupportAssistant

1. Click **+ Add a topic**.

1. Select **Add from description with Copilot**.

1. Enter the following details:

   - **Name:** `HardwareSupportAssistant`
   - **Description:**

      ```
      Create a hardware support topic that handles all common device issues, including laptops, mice, keyboards, monitors, printers, headphones, docking stations, network adapters, and any other device. Begin by asking the user which device they are having trouble with and save this selection as a variable, then ask them to describe the issue in their own words and save that as another variable. Provide troubleshooting steps based on the selected device: for laptops, include steps for slow performance, freezing, overheating, slow boot, high CPU or memory usage, updates, restart, disk cleanup, and malware checks; for printers, include steps for offline issues, paper jams, blank pages, print queue problems, restarting the spooler, reconnecting cables, reloading paper, and power cycling; for mice and keyboards, include USB or Bluetooth checks, battery checks, driver checks, cleaning stuck keys, and re-pairing; for monitors, include steps for no display, flickering, resolution problems, cable or port checks, brightness and power checks; for headphones and microphones, include audio settings, mic testing, Bluetooth reconnecting, resetting, and driver updates; and for docking stations or network adapters, include cable checks, restarting the dock, firmware checks, and adapter resets. For any "other device," provide general troubleshooting such as checking cables, restarting the device, and verifying drivers. After the troubleshooting steps, ask the user whether the issue is resolved. If not, offer to create a support ticket. When creating the ticket, generate a subject like "Hardware Issue – <device>" and a description that includes the user's reported issue details and device type, and map these values to the Freshdesk Power Automate flow as the Subject and Description inputs.
      ```

1. Click **Create** or **Generate**.

1. Review and customize the generated topic:

   - **Trigger phrases:** Verify it includes phrases like:
   - "My laptop is slow"
   - "Printer not working"
   - "Mouse not responding"
   - "Keyboard issue"
   - "Monitor problems"
   - "Hardware issue"
   - "Device not working"

1. Review the conversation flow:

1. **Important:** If you see an error such as **PowerFxError** or a limited scope issue:
   - Click the ellipsis (**...**) on the affected node.
   - Select **Delete**.

1. Click **Save**.

### Step 5: Review All Topics

1. In the **Topics** list, verify you now have 3 custom topics:

   - CredentialResetSupport
   - VPNConnectivitySupport
   - HardwareSupportAssistant

1. Ensure all topics are **enabled** (toggle should be on).

### Step 6: Connect Topics to Freshdesk Flow

Now connect each topic to your published **Freshdesk** flow. The AI-generated topics should already have the conversation flow with variables captured. You'll add the action to call the Freshdesk flow when escalation is needed.

#### Connect CredentialResetSupport Topic to Flow:

1. Open **CredentialResetSupport** topic in the editor.

1. Navigate through the topic flow and find the appropriate place where escalation to ticket creation should happen.

1. Add the **Freshdesk** tool immediately after the message where you inform the user that a support ticket will be created:

   - Click the **+** icon.
   - Select **Add a tool**.
   - Select **Freshdesk**.

1. Map the flow inputs using the ellipsis (**...**) icon:

   - For **Subject**, select the appropriate topic variable such as **Username**.
   - For **Description**, select the relevant topic variable such as **ResetIssue**.

      > **Note:** If your topic doesn't have all the required variables, add **Question** nodes to collect missing information before calling the flow.

1. Add a confirmation message after the flow action and click **Save**.

#### Connect VPNConnectivitySupport Topic to Flow:

1. Open **VPNConnectivitySupport** topic in the editor.

1. Navigate through the topic flow and find the appropriate place for ticket creation.

1. Add the **Freshdesk** tool immediately after the message where you inform the user that the issue is escalated:

   - Click the **+** icon.
   - Select **Add a tool**.
   - Select **Freshdesk**.

1. Map the flow inputs using the ellipsis (**...**) icon:

   - For **Subject**, select the appropriate topic variable such as **Location**.
   - For **Description**, select the relevant topic variable such as **ErrorMessage**.

      > **Note:** If your topic doesn't capture all necessary information, add **Question** nodes to collect missing details before calling the flow.

1. Add a confirmation message after the flow action and click **Save**.

#### Connect HardwareSupportAssistant Topic to Flow:

1. Open **HardwareSupportAssistant** topic in the editor.

1. Navigate through the topic flow and find the escalation point.

1. Add the **Freshdesk** tool immediately after the message where you inform the user that a support ticket will be created:

   - Click the **+** icon.
   - Select **Add a tool**.
   - Select **Freshdesk**.

1. Map the flow inputs using the ellipsis (**...**) icon:

   - For **Subject**, select the appropriate topic variable such as **DeviceType**.
   - For **Description**, select the relevant topic variable such as **IssueDescription**.

      > **Note:** If your topic doesn't have the necessary variables, add **Question** nodes to gather the required information before calling the flow.

1. Add a confirmation message after the flow action and click **Save**.

## Success Criteria
- Use Copilot Studio's generative AI to create 3 topics
- Review All Topics
- Connect Topics to Freshdesk Flow

## Additional Resources
- [Create topics with Copilot](https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics)  
- [Use generative AI for topic creation](https://learn.microsoft.com/microsoft-copilot-studio/nlu-authoring)  

Now, click **Next** to continue to **Challenge 05: Test Your IT Helpdesk Copilot End-to-End**.
