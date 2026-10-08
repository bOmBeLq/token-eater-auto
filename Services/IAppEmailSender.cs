namespace TokenEaterAuto.Services;

public interface IAppEmailSender
{
    Task SendEmailAsync(string recipient, string subject, string htmlBody);
}
