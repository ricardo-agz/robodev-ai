const BaseMailer = require('./baseMailer')
$$DOTENV$$

class $$MailerName$$ extends BaseMailer {
  constructor(senderAddress) {
    this.sender = senderAddress;
  }

  $$TEMPLATES$$
}

module.exports = $$MailerName$$;