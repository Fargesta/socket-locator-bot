import db_context.models as models

async def setup_roles():
    admin_role = await models.TG_role.get_or_none(code="ADMIN")
    if not admin_role:
        await models.TG_role.create(
            name="Admin",
            code="ADMIN",
            description="Administrator role with full access to the system."
        )

    user_role = await models.TG_role.get_or_none(code="USER")
    if not user_role:
        await models.TG_role.create(
            name="User",
            code="USER",
            description="Standard user role with limited access."
        )

    moderator_role = await models.TG_role.get_or_none(code="MODER")
    if not moderator_role:
        await models.TG_role.create(
            name="Moderator",
            code="MODER",
            description="Moderator role with permissions to manage user content."
        )

    guest_role = await models.TG_role.get_or_none(code="GUEST")
    if not guest_role:
        await models.TG_role.create(
            name="Guest",
            code="GUEST",
            description="Guest role with minimal access."
        )