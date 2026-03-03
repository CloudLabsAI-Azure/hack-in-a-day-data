# Challenge 06: Publish Your Agent to Microsoft Teams

## Introduction
The final step is to deploy your IT Helpdesk Copilot to Microsoft Teams, making it accessible to employees in your organization. Teams is the perfect channel for IT support—employees can get help directly where they already collaborate and communicate.

In this challenge, you will publish your agent, add it to Teams, and test the complete user experience.

## Challenge Objectives
- Publish the Agent to Microsoft Teams
- Test the Agent in Microsoft Teams

## Steps to Complete

### Step 1: Publish the Agent to Microsoft Teams

1. In **Copilot Studio**, ensure you're in your **IT Support Copilot** Agent.

1. Select **Channels**, and then choose **Teams and Microsoft 365 Copilot** under *Microsoft channels*.

1. Uncheck the **Make agent available in Microsoft 365 Copilot** checkbox, review the **Agent preview** section, and then click **Add channel**.

1. After the channel is added successfully, select **See agent in Teams** under *Agent preview*.

1. If prompted with **Open Microsoft Teams?**, select **Cancel** to proceed.

1. On the Teams welcome page, select **Use the web app instead** to continue in the browser.

1. In Microsoft Teams, select **Add** to install the **IT Support Copilot** app.

   > **Note:** If you do not see the **Add** option, return to the previous steps and reperform.

1. After the app is added successfully, select **Open** to launch **IT Support Copilot**.

### Step 2: Test the Agent in Microsoft Teams

1. In the **IT Support Copilot** chat, type the following and send the message:
   ```
   I forgot my password
   ```

1. Follow the conversation:
   - Provide your username when asked
   - Review the self-service reset instructions
   - When asked if resolved, say: **No**
   - Confirm ticket creation

1. Try another test by typing the following:
   ```
   VPN won't connect from home
   ```

1. Follow the conversation and escalate to ticket creation.

1. Verify ticket appears in Freshdesk with correct details.

1. Test a knowledge base query by typing the following:
   ```
   What are the steps to reset my password?
   ```

1. **Expected:** The agent should provide instructions from the knowledge base without offering to create a ticket.

<validation step="6d77e727-80a0-4147-8484-e70b51cd78e3" />
 
> **Congratulations** on completing the Challenge! Now, it's time to validate it. Here are the steps:
> - Hit the Validate button for the corresponding Challenge. If you receive a success message, you can proceed to the next Challenge. 
> - If not, carefully read the error message and retry the step, following the instructions in the lab guide.
> - If you need any assistance, please contact us at cloudlabs-support@spektrasystems.com. We are available 24/7 to help.

## Success Criteria
- Publish the Agent to Microsoft Teams
- Test the Agent in Microsoft Teams

## Additional Resources
- [Publish your copilot](https://learn.microsoft.com/microsoft-copilot-studio/publication-fundamentals-publish-channels)  
- [Deploy to Microsoft Teams](https://learn.microsoft.com/microsoft-copilot-studio/publication-add-bot-to-microsoft-teams)  
- [Analyze copilot performance](https://learn.microsoft.com/microsoft-copilot-studio/analytics-overview)  
- [Share your copilot](https://learn.microsoft.com/microsoft-copilot-studio/admin-share-bots)

## Congratulations!

You have successfully built an **AI-powered IT Helpdesk Automation Copilot** using Microsoft Copilot Studio!

### Real-World Applications:
This solution can transform IT operations across:
- **IT Support & Helpdesk** - Password resets, VPN issues, hardware troubleshooting
- **Employee Onboarding** - Equipment setup, account provisioning, access requests
- **Service Desk Automation** - Ticket triage, incident management, self-service support
- **Infrastructure Management** - Network diagnostics, system monitoring alerts
- **Software Support** - Application troubleshooting, license management, update assistance
- **Security & Compliance** - Access reviews, security incident reporting, policy enforcement

Congratulations on completing this challenge!
