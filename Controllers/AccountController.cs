using System.Text.Encodings.Web;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.WebUtilities;
using TokenEaterAuto.Models;
using TokenEaterAuto.Services;

namespace TokenEaterAuto.Controllers;

public sealed class AccountController(
    UserManager<IdentityUser> userManager,
    SignInManager<IdentityUser> signInManager,
    IAppEmailSender emailSender) : Controller
{
    [AllowAnonymous]
    public IActionResult Register() => View();

    [HttpPost, AllowAnonymous]
    public async Task<IActionResult> Register(RegisterViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var user = new IdentityUser { UserName = model.Email, Email = model.Email };
        var result = await userManager.CreateAsync(user, model.Password);
        if (!result.Succeeded)
        {
            AddErrors(result);
            return View(model);
        }

        var token = await userManager.GenerateEmailConfirmationTokenAsync(user);
        var encodedToken = WebEncoders.Base64UrlEncode(System.Text.Encoding.UTF8.GetBytes(token));
        var link = Url.Action(nameof(ConfirmEmail), "Account", new { userId = user.Id, token = encodedToken }, Request.Scheme)!;
        await emailSender.SendEmailAsync(
            model.Email,
            "Confirm your Token Eater account",
            $"<p>Welcome to Token Eater.</p><p><a href=\"{HtmlEncoder.Default.Encode(link)}\">Confirm your email address</a></p>");

        return RedirectToAction(nameof(RegisterConfirmation));
    }

    [AllowAnonymous]
    public IActionResult RegisterConfirmation() => View();

    [AllowAnonymous]
    public async Task<IActionResult> ConfirmEmail(string? userId, string? token)
    {
        if (string.IsNullOrWhiteSpace(userId) || string.IsNullOrWhiteSpace(token))
        {
            return View("ConfirmationFailed");
        }

        var user = await userManager.FindByIdAsync(userId);
        if (user is null)
        {
            return View("ConfirmationFailed");
        }

        IdentityResult result;
        try
        {
            var decodedToken = System.Text.Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(token));
            result = await userManager.ConfirmEmailAsync(user, decodedToken);
        }
        catch (FormatException)
        {
            return View("ConfirmationFailed");
        }

        return View(result.Succeeded ? "ConfirmEmail" : "ConfirmationFailed");
    }

    [AllowAnonymous]
    public IActionResult Login() => View();

    [HttpPost, AllowAnonymous]
    public async Task<IActionResult> Login(LoginViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var result = await signInManager.PasswordSignInAsync(
            model.Email,
            model.Password,
            model.RememberMe,
            lockoutOnFailure: true);

        if (result.Succeeded)
        {
            return RedirectToAction("Index", "Dashboard");
        }

        ModelState.AddModelError(string.Empty, "Invalid login attempt or unconfirmed email address.");
        return View(model);
    }

    [HttpPost, Authorize]
    public async Task<IActionResult> Logout()
    {
        await signInManager.SignOutAsync();
        return RedirectToAction("Index", "Home");
    }

    [AllowAnonymous]
    public IActionResult ForgotPassword() => View();

    [HttpPost, AllowAnonymous]
    public async Task<IActionResult> ForgotPassword(ForgotPasswordViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var user = await userManager.FindByEmailAsync(model.Email);
        if (user is not null && await userManager.IsEmailConfirmedAsync(user))
        {
            var token = await userManager.GeneratePasswordResetTokenAsync(user);
            var encodedToken = WebEncoders.Base64UrlEncode(System.Text.Encoding.UTF8.GetBytes(token));
            var link = Url.Action(nameof(ResetPassword), "Account", new { email = model.Email, token = encodedToken }, Request.Scheme)!;
            await emailSender.SendEmailAsync(
                model.Email,
                "Reset your Token Eater password",
                $"<p><a href=\"{HtmlEncoder.Default.Encode(link)}\">Reset your password</a></p>");
        }

        return RedirectToAction(nameof(ForgotPasswordConfirmation));
    }

    [AllowAnonymous]
    public IActionResult ForgotPasswordConfirmation() => View();

    [AllowAnonymous]
    public IActionResult ResetPassword(string? email, string? token)
    {
        if (string.IsNullOrWhiteSpace(email) || string.IsNullOrWhiteSpace(token))
        {
            return BadRequest();
        }

        return View(new ResetPasswordViewModel { Email = email, Token = token });
    }

    [HttpPost, AllowAnonymous]
    public async Task<IActionResult> ResetPassword(ResetPasswordViewModel model)
    {
        if (!ModelState.IsValid)
        {
            return View(model);
        }

        var user = await userManager.FindByEmailAsync(model.Email);
        if (user is null)
        {
            return RedirectToAction(nameof(ResetPasswordConfirmation));
        }

        IdentityResult result;
        try
        {
            var decodedToken = System.Text.Encoding.UTF8.GetString(WebEncoders.Base64UrlDecode(model.Token));
            result = await userManager.ResetPasswordAsync(user, decodedToken, model.Password);
        }
        catch (FormatException)
        {
            ModelState.AddModelError(string.Empty, "The password reset link is invalid or expired.");
            return View(model);
        }

        if (!result.Succeeded)
        {
            AddErrors(result);
            return View(model);
        }

        return RedirectToAction(nameof(ResetPasswordConfirmation));
    }

    [AllowAnonymous]
    public IActionResult ResetPasswordConfirmation() => View();

    [AllowAnonymous]
    public IActionResult AccessDenied() => View();

    private void AddErrors(IdentityResult result)
    {
        foreach (var error in result.Errors)
        {
            ModelState.AddModelError(string.Empty, error.Description);
        }
    }
}
