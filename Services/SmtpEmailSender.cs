using System.Net;
using System.Net.Mail;
using Microsoft.Extensions.Options;

namespace TokenEaterAuto.Services;

public sealed class SmtpEmailSender(IOptions<SmtpOptions> options) : IAppEmailSender
{
    private readonly SmtpOptions _options = options.Value;

    public async Task SendEmailAsync(string recipient, string subject, string htmlBody)
    {
        if (string.IsNullOrWhiteSpace(_options.Host) || string.IsNullOrWhiteSpace(_options.FromAddress))
        {
            throw new InvalidOperationException("SMTP host and sender address must be configured.");
        }

        using var message = new MailMessage
        {
            From = new MailAddress(_options.FromAddress, _options.FromName),
            Subject = subject,
            Body = htmlBody,
            IsBodyHtml = true
        };
        message.To.Add(recipient);

        using var smtpClient = new SmtpClient(_options.Host, _options.Port)
        {
            EnableSsl = _options.EnableSsl
        };

        if (!string.IsNullOrWhiteSpace(_options.UserName))
        {
            smtpClient.Credentials = new NetworkCredential(_options.UserName, _options.Password);
        }

        await smtpClient.SendMailAsync(message);
    }
}
