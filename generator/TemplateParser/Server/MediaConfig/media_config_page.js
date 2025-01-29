const AWS = require('aws-sdk');
// Set your AWS credentials and region
AWS.config.update({
    accessKeyId: "YOUR_ACCESS_KEY_ID",
    secretAccessKey: "YOUR_SECRET_ACCESS_KEY",
    region: "REGION"
});

module.exports = AWS;