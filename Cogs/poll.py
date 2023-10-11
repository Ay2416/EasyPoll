# Discord bot import
import discord
import emoji
from discord import app_commands
from discord.ext import commands

# my program import
# none

class poll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    # /poll
    @app_commands.command(name="poll",description="リアクションタイプのアンケートを作成します。")
    @app_commands.describe(item="質問の項目を「,」で区切って入力してください。")
    @app_commands.describe(message_content="※入力しなくても可 / 表示させたいメッセージを入れてください。")
    @app_commands.describe(message_content="※入力しなくても可 / リアクションのモードを選択してください。（数字：最大項目数10個、アルファベッド：最大項目数：26個）")
    @app_commands.guild_only()
    @app_commands.choices(reaction_type=[discord.app_commands.Choice(name="数字",value="num"),discord.app_commands.Choice(name="アルファベッド",value="alphabet")])
    async def poll_command(self, interaction: discord.Interaction, item:str, message_content:str=None, reaction_type:str=None):
        
        num_reactions = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
        alphabet_reactions = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:', ':regional_indicator_d:', ':regional_indicator_e:',
                              ':regional_indicator_f:', ':regional_indicator_g:', ':regional_indicator_h:', ':regional_indicator_i:', ':regional_indicator_j:',
                              ':regional_indicator_k:', ':regional_indicator_l:', ':regional_indicator_m:', ':regional_indicator_n:', ':regional_indicator_o:', 
                              ':regional_indicator_p:', ':regional_indicator_q:', ':regional_indicator_r:', ':regional_indicator_s:', ':regional_indicator_t:',
                              ':regional_indicator_u:', ':regional_indicator_v:', ':regional_indicator_w:', ':regional_indicator_x:', ':regional_indicator_y:',
                              ':regional_indicator_z:']
        alphabet_reactions_unicode = ['🇦', '🇧', '🇨', '🇩', '🇪',
                                      '🇫', '🇬', '🇭', '🇮', '🇯',
                                      '🇰', '🇱', '🇲', '🇳', '🇴', 
                                      '🇵', '🇶', '🇷', '🇸', '🇹',
                                      '🇺', '🇻', '🇼', '🇽', '🇾',
                                      '🇿']
        
        # Noneである場合代入
        if reaction_type == None:
            reaction_type = 'num'

        if message_content == None:
            message_content = '下記にリアクションをして投票してください！'
        
        # 項目を分割する
        try:
            item_list = item.split(',')
        except Exception as e:
            embed=discord.Embed(title="エラーが発生しました。", color=0xff0000)
            embed.add_field(name="入力した項目を確認してください。（区切り文字などが間違っている可能性があります。）", value="", inline=False)
            
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return
        
        # 項目数が超えていないかを確認
        content_num = 0

        if reaction_type == 'num':
            content_num = len(num_reactions)
        else:
            content_num = len(alphabet_reactions)

        if content_num < len(item_list):
            embed=discord.Embed(title="入力された項目が多すぎます！", color=0xff0000)
            embed.add_field(name="このリアクションタイプでの最大項目数は" + str(content_num) + "です。", value="", inline=False)
            
            await interaction.response.send_message(embed=embed,ephemeral=True)
            return

        # メッセージに対応する項目を説明する部分を追加
        message_content += '\n'

        for i in range(0, len(item_list)):
            if reaction_type == 'num':
                message_content += "\n" + num_reactions[i] + "：" + item_list[i]
            else:
                message_content += "\n" + alphabet_reactions[i] + "：" + item_list[i]

        # embedを作り、投稿
        embed=discord.Embed(title="", color=0xfafad2)
        embed.add_field(name="アンケートコマンドが使用されました。", value=message_content, inline=False)

        await interaction.response.send_message(embed=embed,ephemeral=False)

        # リアクションを付与していく
        # 直近のメッセージを取得？
        message = await interaction.original_response()

        for i in range(0, len(item_list)):
            if reaction_type == 'num':
                await message.add_reaction(emoji.emojize(num_reactions[i], language='alias'))
            else:
                await message.add_reaction(alphabet_reactions_unicode[i])

async def setup(bot: commands.Bot):
    await bot.add_cog(poll(bot))