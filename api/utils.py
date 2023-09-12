import africastalking


def send_sms_alert(customer_name, order_item, recipient_phone):
    sms = africastalking.SMS
    message = 'Hello {customer_name}, your order for {order_item} has been added.'
    recipients = [recipient_phone]

    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print('An error occurred while sending the SMS: {str(e)}')

