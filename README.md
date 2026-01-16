# TermLink

Hello! This is TermLink, a new messaging platform I'm designing. It's a terminal app to keep it fast and lightweight, but it's still important to keep it user-friendly even while being technical.

Unlike most messaging platforms, I'm not expecting to handle servers—the reason being they're not very stable. This will be a fully stable option.

## How It Works

One user has to be a host (they can still send messages) while everyone else connects to that host. The host will supply the port and IP onto this website, then every user will connect to the host using that IP and port.

## Security Risks

It's important to bring up the risks of exposing your IP and port forwarding.

**Exposing your public IP:**
- Reveals your approximate location and ISP
- Makes you a direct target for scanning and DDoS attacks

**Port forwarding risks:**
- Creates a direct path from the internet to your internal device
- Vulnerable or misconfigured services can be exploited
- Common ports (SSH, RDP, web) get hammered by automated bots

**Mitigations:**
- Strong authentication (SSH keys, no default passwords)
- Keep software updated
- Use non-standard ports
- Consider alternatives like Tailscale or Cloudflare Tunnels that avoid opening ports entirely

Now, it is important to say—every website you visit gets your public IP address. It's not very easy to keep it private. Anyway, it's up to you how you want to do this. I suggest you use a VPN if you're worried about it, and if you're not you can just do it normally.
