{
    "name": "Simple Sale Filter Action (Python + XML)",
    "version": "1.0",
    "category": "Sales",
    "summary": "Menu action to show confirmed Sales Orders",
    "author": "Your Company",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/action_menu.xml",
    ],

    "installable": True,
    "application": False,
}
