using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using TokenEaterAuto.Models;

namespace TokenEaterAuto.Controllers;

[Authorize]
public sealed class ProfileController(UserManager<IdentityUser> userManager) : Controller
{
    public async Task<IActionResult> Index()
    {
        var user = await userManager.GetUserAsync(User);
        if (user is null)
        {
            return Challenge();
        }

        return View(new ProfileViewModel(user.Email ?? string.Empty));
    }
}
