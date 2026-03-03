# Challenge 03: Create Agent Flows for Actions

## Introduction
Your copilot can answer questions using the Contoso knowledge base, but what if employees want to receive a document via email or submit a request to their team? In this challenge, you'll create two agent flows that enable your copilot to take actions beyond just answering questions.

These flows will be created first so they're ready to use when you build conversational topics in Challenge 4.

## Challenge Objectives
- Create an agent flow to email documents to employees
- Create an agent flow to send requests to Microsoft Teams
- Verify both flows are configured correctly
- Prepare flows for integration with agent topics in the next challenge

## Steps to Complete

### Step 1: Access Agent Flows in Copilot Studio

1. In **Copilot Studio**, ensure your **Internal Knowledge Navigator** agent is open.

1. In the left navigation pane, select **Flows**.

1. You will see the **Agent flows** page with options to create new flows.

### Step 2: Create Flow 1 - Email Document to Employee

1. On the **Agent flows** page, click **+ New agent flow**.

1. This will open the flow designer.

### Step 3: Configure Flow 1 Trigger and Inputs

1. In the **Add a trigger** pane, search for **When an agent calls the flow**, and then select **When an agent calls the flow** under **Skills**.

1. In the trigger node, click **+ Add an input**.

1. Select **Text** as the input type.

1. Enter **EmployeeEmail** as the input name and press Enter.

1. Click **+ Add an input** again and add:
   - Type: **Text**
   - Name: **DocumentName**

1. Click **+ Add an input** one more time and add:
   - Type: **Text**
   - Name: **DocumentDescription**

1. You should now have 3 input parameters: EmployeeEmail, DocumentName, and DocumentDescription.

### Step 4: Add Email Action

1. Below the trigger node, click on **(+)** to add a new step.

1. In the search box, type **Send an email** and select **Send an email (V2)** from **Office 365 Outlook**.

1. If prompted to sign in, use Lab credentials: **<inject key="AzureAdUserEmail"></inject>**

1. Configure the email action:

   - **To:** Enter **<inject key="AzureAdUserEmail"></inject>**
   
   - **Subject:** Type: `Your Requested Document - ` and then select **DocumentName** from dynamic content.
   
   - **Body:** Enter the following text and add dynamic content where indicated:

   ```
   Hello,

   As requested, here is information about the document you requested.

   Document: [Click and add DocumentName dynamic content]
   Description: [Click and add DocumentDescription dynamic content]

   You can access this document through the Contoso SharePoint site or contact your department for more details.

   Best regards,
   Internal Knowledge Navigator
   ```

1. Click **Publish** in the top-right corner.

### Step 5: Rename Flow 1 - Email Document to Employee

1. Click **Flow** to return to the Flows page.

1. In the Flow page, select the **Overview** tab to view the flow details.

1. In the **Overview** tab, select **Edit** to modify the flow details.

1. In the flow designer, click on the flow name at the top (it will have a default name).

1. Change the name to the following:
   ```
   Email Document Flow
   ```

1. Click **Save** to save the renamed flow.

### Step 6: Create Flow 2 - Send Request to Teams

1. Navigate back to the **Flows** page.

1. Click **+ New agent flow**.

1. This will open the flow designer.

### Step 7: Configure Flow 2 Trigger and Inputs

1. In the **Add a trigger** pane, search for **When an agent calls the flow**, and then select **When an agent calls the flow** under **Skills**.

1. In the trigger node, click **+ Add an input**.

1. Select **Text** as the input type.

1. Add the following input parameters one by one:

   1. **EmployeeName** (Text)
   1. **EmployeeEmail** (Text)
   1. **RequestType** (Text)
   1. **RequestDetails** (Text)

1. You should now have 4 input parameters defined.

### Step 8: Add Teams Action

1. Below the trigger node, click on **(+)** to add a new step.

1. In the search box, type **Post message** and select **Post message in a chat or channel** from **Microsoft Teams**.

1. If prompted to sign in, use Lab credentials: **<inject key="AzureAdUserEmail"></inject>**

1. Configure the Teams action:

   - **Post as:** Flow bot
   
   - **Post in:** Channel

   - **Team:** Select Exisitng

   - **Channel:** **Document Request-<inject key="DeploymentID"></inject>**
   
      ```
      New Employee Request Submitted

      Employee: [Add EmployeeName dynamic content]
      Email: [Add EmployeeEmail dynamic content]
      Request Type: [Add RequestType dynamic content]

      Details:
      [Add RequestDetails dynamic content]

      Please review and respond to this request.
      ```

1. Click **Publish** in the top-right corner.

1. The flow is now saved with a default name. You'll rename it next.

### Step 9: Rename Flow 2 - Send Request to Teams

1. Click **Flow** to return to the Flows page.

1. In the Flow page, select the **Overview** tab to view the flow details.

1. In the **Overview** tab, select **Edit** to modify the flow details.

1. In the flow designer, click on the flow name at the top.

1. Change the name to the following:
   ```
   Request Teams Flow
   ```

1. Click **Save** to save the renamed flow.

### Step 10: Verify Both Flows are Created and Renamed

1. On the **Flows** page, you should now see both agent flows listed with their correct names:
   - Email Document Flow
   - Request Teams Flow

1. Both flows should show as **On** or **Active** status.

   > **Note:** These flows are now ready to be used in your agent topics in Challenge 4.

<validation step="718fdc4b-852f-46bb-883c-5a5c8ae52fef" />
 
> **Congratulations** on completing the Challenge! Now, it's time to validate it. Here are the steps:
> - Hit the Validate button for the corresponding Challenge. If you receive a success message, you can proceed to the next Challenge. 
> - If not, carefully read the error message and retry the step, following the instructions in the lab guide.
> - If you need any assistance, please contact us at cloudlabs-support@spektrasystems.com. We are available 24/7 to help.

## Success Criteria
- Created **Email Document to Employee** agent flow
- Created **Send Request to Teams** agent flow
- Both flows have the correct input parameters configured
- Both flows are saved and active in Copilot Studio
- Flows are ready to be used in conversational topics in Challenge 4

## Additional Resources
- [Create flows for Microsoft Copilot Studio](https://learn.microsoft.com/microsoft-copilot-studio/advanced-flow)
- [Use flows in Copilot Studio](https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-flows)
- [Office 365 Outlook connector](https://learn.microsoft.com/connectors/office365/)
- [Microsoft Teams connector](https://learn.microsoft.com/connectors/teams/)

Click **Next** at the bottom of the page to proceed to the next page.

   ![](./media/auto-it-gt-gr-g6.png)