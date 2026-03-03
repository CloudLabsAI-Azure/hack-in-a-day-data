# Challenge 05: Test Your IT Helpdesk Copilot End-to-End

## Introduction
Now that you've built your IT Helpdesk Copilot with 3 topics, a reusable Freshdesk flow, and knowledge base integration, it's time to thoroughly test the complete solution. End-to-end testing ensures all components work together seamlessly—from user input to ticket creation in Freshdesk.

In this challenge, you will test all 3 topics comprehensively, verify Freshdesk flow integration, confirm tickets are created in Freshdesk, and validate the entire user experience.

## Challenge Objectives
- Prepare Your Test Environment
- Test 1 IT Support Copilot
- Test 2 IT Support Copilot
- Test 3 Knowledge Base Integration
- Verify Ticket Details in Freshdesk

## Steps to Complete

### Step 1: Prepare Your Test Environment

1. Open your **IT Support Copilot** in Copilot Studio.

1. Click on **Publish**.

1. In the **Publish this agent** pane, click on **Publish**.

1. Wait for the **IT Support Copilot** to be **published**.

1. In a separate browser tab, navigate back to the **Freshdesk** portal.

1. Keep both windows visible for testing.

### Step 2: Test 1 IT Support Copilot

1. Click the **Test** button to open the test panel on the right side.

1. Type the following trigger phrase:
   ```
   I forgot my password
   ```

1. Follow the conversation flow:
   - Provide username when asked
   - Review the self-service reset instructions
   - When asked if you need to escalate, say: **Yes, create a ticket**

1. Verify the agent:
   - Calls the Freshdesk flow
   - Displays confirmation message
   - Shows appropriate response

1. Switch to Freshdesk portal → Go to **Tickets** section.

1. Verify the new ticket:
   - **Subject:** Should contain "Password Reset Assistance"
   - **Description:** Should mention username and issue details
   - **Priority:** Medium
   - **Requester Email:** Should match your email
   - **Status:** Open

### Step 3: Test 2 IT Support Copilot

1. Click **New test session** to start a fresh conversation.

1. Type the following:
   ```
   VPN won't connect
   ```

1. Follow the conversation:
   - Provide error details
   - Answer troubleshooting questions
   - Request ticket creation

1. Ensure the topic triggers correctly and provides relevant troubleshooting steps.

1. When ticket is created, verify:
   - Confirmation message is displayed
   - Ticket appears in Freshdesk

1. In **Freshdesk**, check the new ticket:
   - **Subject:** Should contain "Connectivity Issue" with location
   - **Description:** Should include error message and location details
   - **Priority:** Medium
   - **Status:** Open

### Step 4: Test 3 Knowledge Base Integration

Test if your agent can answer questions directly from the knowledge base without creating tickets.

1. Click **New test session** to start a fresh conversation.

1. Ask a general IT question by typing the following:
   ```
   How do I clear my browser cache?
   ```

1. Verify the agent:
   - Provides a direct answer from knowledge base
   - Does NOT trigger a topic unnecessarily
   - Offers helpful instructions

1. Try another knowledge base query by typing the following:
   ```
   What are the system requirements for our VPN client?
   ```

1. Check if the response comes from the uploaded knowledge base.

1. If responses are generic, verify:
   - Knowledge sources are enabled in **Settings** → **Generative AI**
   - **IT_Support_QA.pdf** is uploaded and indexed

### Step 5: Verify Ticket Details in Freshdesk

1. In **Freshdesk**, go to **Tickets** → View all open tickets.

1. Review the newly created tickets.

## Success Criteria
- Prepare Your Test Environment
- Test 1 IT Support Copilot
- Test 2 IT Support Copilot
- Test 3 Knowledge Base Integration
- Verify Ticket Details in Freshdesk

## Additional Resources
- [Test your copilot](https://learn.microsoft.com/microsoft-copilot-studio/authoring-test-bot)  
- [Debug topic flows](https://learn.microsoft.com/microsoft-copilot-studio/authoring-create-edit-topics)  
- [Freshdesk API troubleshooting](https://developers.freshdesk.com/api/)

Now, click **Next** to continue to **Challenge 06: Publish Your Copilot to Microsoft Teams**.
