import discord

async def CreateMuteRole(interaction: discord.Interaction):
   await interaction.guild.create_role(
      name = 'Mute',
      permissions = discord.Permissions(4296082432),
      colour = discord.Color.dark_red(),
      hoist = False,
      mentionable = False,
      reason = 'Mute role (keep all roles).'
   )

async def CreateHardMuteRole(interaction: discord.Interaction):
   await interaction.guild.create_role(
      name = 'Hard Mute',
      permissions = discord.Permissions(4296082432),
      colour = discord.Colour.dark_red(),
      hoist = False,
      mentionable = False,
      reason = 'Hard mute role (remove all roles).'
   )

m_overMute = discord.PermissionOverwrite(
   add_reactions = False,
   administrator = False,
   attach_files = False,
   ban_members = False,
   change_nickname = False,
   connect = False,
   create_events = False,
   create_expressions = False,
   create_instant_invite = False,
   create_polls = False,
   create_private_threads = False,
   create_public_threads = False,
   deafen_members = False,
   embed_links = False,
   external_emojis = False,
   kick_members = False,
   manage_channels = False,
   manage_emojis = False,
   manage_emojis_and_stickers = False,
   manage_events = False,
   manage_expressions = False,
   manage_guild = False,
   manage_messages = False,
   manage_nicknames = False,
   manage_permissions = False,
   manage_roles = False,
   manage_threads = False,
   manage_webhooks = False,
   mention_everyone = False,
   moderate_members = False,
   move_members = False,
   mute_members = False,
   read_message_history = True, #
   read_messages = True, #
   request_to_speak = False,
   send_messages = True, #
   send_messages_in_threads = False,
   send_polls = False,
   send_tts_messages = False,
   send_voice_messages = False,
   speak = True, #
   stream = True, #
   use_application_commands = False,
   use_embedded_activities = True, #
   use_external_apps = False,
   use_external_emojis = False,
   use_external_sounds = False,
   use_external_stickers = False,
   use_soundboard = False,
   use_voice_activation = True, #
   view_audit_log = False,
   view_channel = True, #
   view_guild_insights = False
)

hm_overMute = discord.PermissionOverwrite(
   add_reactions = False,
   administrator = False,
   attach_files = False,
   ban_members = False,
   change_nickname = False,
   connect = False,
   create_events = False,
   create_expressions = False,
   create_instant_invite = False,
   create_polls = False,
   create_private_threads = False,
   create_public_threads = False,
   deafen_members = False,
   embed_links = False,
   external_emojis = False,
   kick_members = False,
   manage_channels = False,
   manage_emojis = False,
   manage_emojis_and_stickers = False,
   manage_events = False,
   manage_expressions = False,
   manage_guild = False,
   manage_messages = False,
   manage_nicknames = False,
   manage_permissions = False,
   manage_roles = False,
   manage_threads = False,
   manage_webhooks = False,
   mention_everyone = False,
   moderate_members = False,
   move_members = False,
   mute_members = False,
   read_message_history = True, #
   read_messages = True, #
   request_to_speak = False,
   send_messages = True, #
   send_messages_in_threads = False,
   send_polls = False,
   send_tts_messages = False,
   send_voice_messages = False,
   speak = True, #
   stream = True, #
   use_application_commands = False,
   use_embedded_activities = True, #
   use_external_apps = False,
   use_external_emojis = False,
   use_external_sounds = False,
   use_external_stickers = False,
   use_soundboard = False,
   use_voice_activation = True, #
   view_audit_log = False,
   view_channel = True, #
   view_guild_insights = False
)