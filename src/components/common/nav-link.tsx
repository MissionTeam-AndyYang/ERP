"use client";

type NavLinkProps = {
  href: string;
  className: string;
  children: React.ReactNode;
};

export function NavLink({ href, className, children }: NavLinkProps) {
  const navigate = () => {
    if (href !== "#") {
      window.location.assign(href);
    }
  };

  return (
    <a
      className={className}
      href={href}
      onMouseDown={(event) => {
        if (event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey) {
          event.preventDefault();
          navigate();
        }
      }}
      onClick={(event) => {
        if (href === "#") {
          return;
        }

        event.preventDefault();
        navigate();
      }}
    >
      {children}
    </a>
  );
}
