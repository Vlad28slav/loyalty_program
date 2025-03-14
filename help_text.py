
supported_func = 'start, help, add_customer, set_program'

help_text =(
    f'Thank you for using our loyalty bot! This is the manual for proper using all features and fuctions of the current bot. '
    f'Current version has following functions: {supported_func}. Let\'s go deep into each of them \n'
    f'/start - This is the very first command that starts the bot. By typing it you agree with conditions and terms of '
    f'use. You can type it only once. Retyping this command has no effect, it will display you your\'s first '
    f'time when you started using this bot from your current Telegram account. Remember that bot recognizes you by your\'s'
    f' account, never by your real or company name \n'
    f'/help - displays this text =)\n'
    f'/set_program - To create a new program write a new valid one. Type /set_program AmountToGetBon'
    f'us BonusSize, for example /set_program 15 1 \n'
    f'If you want to create few levels of reward use following syntaxis : \n/set_prog'
    f'ram AmountToGetBonus BonusSize, AmountToGetBonus BonusSize, AmountToGetBonus'
    f' BonusSize \n For example: \n /set_program 15 1, 20 2, 30 4 \n'
    f'If your bonuses are points or discounts write the amount of discount for every spent euro/dollar/etc like:\n'
    f'/set_program 5 100, 10 300, 20 1000 \n'
    f'Make sure that you write your bonuses from the less atrictive to more attractive. If not, your costomers would not'
    f'receive full amount of deserved reward\n'
    f'/add_customer - The way how you register your customers in this bot. Type "/add_customer CustomerName" to add your '
    f'first customers. For example:\n /add_customer Francesca_Pereira  \n /add_customer Grzegorz_Brzeczyszczykiewicz\n'
    f'Remember that added customer will reserve their name, you can not have more than one Francesca_Pereira so '
    f'in situation that you need to have 2 or more people with similar name you can add them like Francesca_Pereira98, '
    f'or Francesca_Pereira_mainSt. Only you can see your customers but try not to name them like old_guy_with_glasses'
    f'or blondie_with_shepard. In that case you can easily forget who is who.\n'
    f'When you ready with your loyalty bonuses and customers just type their name and purchased amount and bot will calculate'
    f' their reward. for example you have a customer named Paul_Bell and he have bought 12 of your products. '
    f'So type "Paul_Bell 12" or "12 Paul_Bell" to register their purchase.'
    )

