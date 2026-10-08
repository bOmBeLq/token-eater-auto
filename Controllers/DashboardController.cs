using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace TokenEaterAuto.Controllers;

[Authorize]
public sealed class DashboardController : Controller
{
    public IActionResult Index() => View();
}
