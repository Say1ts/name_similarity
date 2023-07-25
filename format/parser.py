from urllib.parse import urlparse, unquote
import tldextract
import re
from functools import lru_cache

from format.exceptions import InvalidEmailException, InvalidQueryException

legal_stopwords_pattern = (r'^ТОО\s|^ИП\s|^АО\s')


def from_legal(name: str) -> str or None:
    target = re.sub(legal_stopwords_pattern, '', name.strip(), flags = re.IGNORECASE)
    return target


def from_instagram(url: str) -> str or None:
    target = url.split('/')[1]
    return target


def from_vk(url: str) -> str or None:
    target = url.split('/')[1]
    if target.startswith('id') or target.startswith('public'):
        return None
    return target


@lru_cache(maxsize=30)
def from_facebook(url: str) -> str or None:
    target = url.split('/')[1]

    if target in ('people', 'groups'):

        target = url.split('/')[2]

        if re.match(r"^\d{4}", target):
            return None

        # decode %D0%90%D0%BD%D0%B4%D1%80%D0%B5%D0%B9
        target = unquote(target)
    elif target.startswith('profile.php'):
        return None
    return target


@lru_cache(maxsize=40)
def from_telegram(url: str) -> str or None:
    target = url.split('/')[1].lstrip('@') \
        # .rstrip('bot') #  may trim "...robot" -> "...r"
    if target.startswith('+'):
        return None
    return target


def from_youtube(url: str) -> str or None:
    target = url.split('/')[1].lstrip('@')
    if target.startswith('watch') or target.startswith('channel'):
        return None
    return target


@lru_cache(maxsize=40)
def to_domains(url: str) -> str or None:
    ''' example: chat.openai.com '''
    if url.startswith('www.'):
        url = url.strip('www.')
    return url.split('/')[0]


def to_main_domains(url: str) -> str or None:
    ''' example: chat.openai '''
    target = to_domains(url)
    extracted = tldextract.extract(target)
    res = extracted.subdomain + '.' + extracted.domain if extracted.subdomain \
        else extracted.domain
    return res


popular_mail_domains = (
    "gmail.com", "mail.ru", "list.ru", "bk.ru", "rambler.ru",
    "inbox.ru", "yandex.ru", "ya.ru", "yandex.kz", "mail.kz"
)

# mail_stopwords = ('sales', 'info')
# stopwords_pattern = '|'.join([f'{word}\W?' for word in mail_stopwords])
mail_stopwords_pattern = ('sales\W?|info\W?')


def from_email(url: str) -> str or None:
    try:
        mail_domain = url.split('@')[1]
    except IndexError:
        #  If index error then email has no @. Email is not valid
        raise InvalidEmailException('Invalid email address')

    if mail_domain in popular_mail_domains:
        #  That domains don't have any semantic mean. We could drop it
        target = url.split('@')[0]
    else:
        target = url
        target = re.sub(mail_stopwords_pattern, '', target)

    return target


def parse_url(url, method) -> str or None:
    parsed_url = urlparse(url)
    if method in (to_domains, from_email, to_main_domains):
        formatted_url = parsed_url.netloc or parsed_url.path
    else:
        formatted_url = parsed_url.path
    try:
        result = method(formatted_url.lower())
        return result
    except Exception as e:
        print(f'Problem parsing url {url}: {e}')
        import traceback
        traceback.print_exc()
        return None



# print(parse_url('https://chat.opEnai.com/?model=text-davinci-002-render-sha', to_main_domains))
# print(parse_url('https://www.openai.com/?model=text-davinci-002-render-sha', to_main_domains))

# print(parse_url('https://vk.com/say1ts', from_vk))
# print(parse_url('https://instagram.com/logic_system?param1=weqweqwe&param2=asdfasdf', from_instagram))
# print(parse_url('instagram.com/abuer_mebel_almaty/?hl=ru', from_instagram))


# print(parse_url('https://www.youtube.com/watch?v=8cwPlMrqgQY', from_youtube), 1)
# print(parse_url('https://www.youtube.com/@Domdivanov', from_youtube), 2)
# print(parse_url('https://www.youtube.com/Domdivanov?23вфыфав', from_youtube), 3)
# print(parse_url('https://www.youtube.com/@Domdivanov/videos', from_youtube), 4)


# print(parse_url('https://t.me/TORUDA_sale_bot', from_telegram))
# print(parse_url('https://t.me/TORUDA_robot', from_telegram))
# print(parse_url('t.me/+77711040004', from_telegram))

# print(parse_url('bravomebel.kazakhstan@gmail.com', from_email))
# print(parse_url('bravomebel.kazakhstan@gmail.com', to_domains))
#
# print(parse_url('info@iclean.kz', from_email))  # -> some-business.com
# print(parse_url('info@some-business.com', from_email))  # -> some-business.com
# print(parse_url('info.some-@business.com', from_email))  # -> some-business.com
# print(parse_url('sales@some-business.com', from_email))  # -> some-business.com
# print(parse_url('sales-some-@business.com', from_email))  # -> some-business.com
# print(parse_url('no_stopwords@some-business.com', from_email))  # -> no_stopwords@some-business.com


# print(from_legal('ТОО ICLEAN QAZAGSTAN'))
# print(from_legal('АО ICLEAN QAZAGSTAN'))

# print(parse_url('https://www.facebook.com/groups/rodniki.moego.sela/', from_facebook))
# print(parse_url('https://www.facebook.com/profile.php?id=100011267862781', from_facebook))
# print(parse_url('https://www.facebook.com/tsydenovsayan', from_facebook))
# print(parse_url('https://www.facebook.com/tsydenovsayan', to_domains))

