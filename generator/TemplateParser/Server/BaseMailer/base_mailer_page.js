const nodemailer = require('nodemailer');
const hbs = require('nodemailer-express-handlebars');
require('dotenv').config();

class Mailer {
  constructor(senderAddress) {
    this.transporter = nodemailer.createTransport({
      port: 465,               // true for 465, false for other ports
      host: process.env.EMAIL_HOST,
      auth: {
        user: process.env.EMAIL_USER,
        pass: process.env.EMAIL_PASSWORD,
      },
      secure: true,
    });

    this.transporter.use('compile', hbs({
      viewEngine: {
        extName: '.hbs',
        partialsDir: './templates/partials',
        layoutsDir: './templates/layouts',
        defaultLayout: 'default.hbs',
      },
      viewPath: './email-templates',
    }));
  }
}