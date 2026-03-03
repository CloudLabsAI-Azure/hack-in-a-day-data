# Challenge 05: Publish Your Agent to Microsoft Teams

## Introduction
The final step is to deploy your Internal Knowledge Navigator agent to Microsoft Teams, making it accessible to employees in your organization. Teams is the perfect channel for knowledge sharing, as employees can get help directly where they already collaborate and communicate.

In this challenge, you will publish your agent, add it to Teams, and test the complete user experience.

## Challenge Objectives
- Publish the agent to Microsoft Teams
- Test topics and flows in Teams

## Steps to Complete

### Step 1: Publish the Agent to Microsoft Teams

1. In **Copilot Studio**, ensure you're in your **Internal Knowledge Navigator** agent.

1. Select **Channels**, and then choose **Teams and Microsoft 365 Copilot** under *Microsoft channels*.

1. Uncheck the **Make agent available in Microsoft 365 Copilot** checkbox, review the **Agent preview** section, and then click **Add channel**.

1. After the channel is added successfully, select **See agent in Teams** under *Agent preview*.

1. If prompted with **Open Microsoft Teams?**, select **Cancel** to proceed.

1. On the Teams welcome page, select **Use the web app instead** to continue in the browser.

1. In Microsoft Teams, select **Add** to install the **Internal Knowledge Navigator** app.

   > **Note:** If you do not see the **Add** option, return to the previous steps and reperform.

1. After the app is added successfully, select **Open** to launch **Internal Knowledge Navigator**.

### Step 2: Test Your Agent in Teams

Test all 3 topics you created in Challenge 4 and the agent's knowledge search capability:

#### Test Knowledge Search:

1. In the agent chat in Teams, type:
   ```
   Where can I find information about employee benefits?
   ```

2. Verify the agent searches the SharePoint knowledge base and provides relevant information.

3. Verify generative answers are provided from the knowledge base.

#### Test EmailDocument Topic:

1. Click **New test session** to start a fresh conversation.

2. Type:
   ```
   Email me a document
   ```

3. Follow the conversation:
   - Provide the document name (e.g., "HR Handbook")
   - Provide your email address
   - Provide a brief description

4. Verify the flow runs and you receive the confirmation message.

5. Check your email inbox (**<inject key="AzureAdUserEmail"></inject>**) to see if the email was delivered.

#### Test SubmitRequest Topic:

1. Click **New test session** to start a fresh conversation.

2. Type:
   ```
   Submit a request to the team
   ```

3. Follow the conversation:
   - Provide your name
   - Provide your email address
   - Select request type from options
   - Describe your request

4. Verify the flow runs and you receive the confirmation message.

5. Check your Microsoft Teams **Document Request** channel to see if the request was posted.

<validation step="09e05d19-df23-42fd-8688-4262e3dcdb95" />
 
> **Congratulations** on completing the Challenge! Now, it's time to validate it. Here are the steps:
> - Hit the Validate button for the corresponding Challenge. If you receive a success message, you can proceed to the next Challenge. 
> - If not, carefully read the error message and retry the step, following the instructions in the lab guide.
> - If you need any assistance, please contact us at cloudlabs-support@spektrasystems.com. We are available 24/7 to help.

## Success Criteria
- Publish the agent to Microsoft Teams
- Test topics and flows in Teams

## Additional Resources
- [Publish your agent](https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels)  
- [Deploy to Microsoft Teams](https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams)  
- [Analyze agent performance](https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview)  
- [Share your agent](https://learn.microsoft.com/microsoft-copilot-studio/admin-share-bots)

## Congratulations!

You have successfully built an **AI-powered Internal Knowledge Navigator Agent** using Microsoft Copilot Studio!

### Real-World Applications:
This solution can transform knowledge management across:
- **HR & Employee Services:** Onboarding, policies, benefits inquiries
- **IT Support:** Self-service help desk, documentation access
- **Compliance & Training:** Policy distribution, procedure guidance
- **Sales Enablement:** Playbooks, product information, pricing guidelines
- **Operations:** Process documentation, vendor management, procurement workflows

Congratulations on completing this challenge! 
