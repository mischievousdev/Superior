from cogs.utils import default

version = "v1.0.0"
invite = "https://discord.gg/qBx2uKZ"
owner = 650890049558282272


def is_owner(ctx):
    return ctx.author.id in owner
