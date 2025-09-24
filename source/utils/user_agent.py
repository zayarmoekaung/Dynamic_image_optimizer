from user_agents import parse

def get_user_agent(request):
    return request.headers.get('User-Agent', '')

def detect_device(user_agent_str):
    try:
        ua = parse(user_agent_str)
        if ua.is_tablet:
            return 'tablet'
        elif ua.is_mobile:
            return 'mobile'
        elif ua.is_pc:
            return 'desktop'
        else:
            return 'desktop'  
    except Exception:
        return 'desktop'  

