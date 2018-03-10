from pick import pick

from utils import state_string_cli


class UserAgentCLI:
    def select_finisher(self, options, state):
        if not isinstance(options, list):
            options = [options]
        option_text = []
        for opt in options:
            option_text.append(str(opt))
        finisher, i = pick(options, 'Choose your Finisher:', '=>')
        return options[i]

    def init_discards(self, styles, bases, state):
        discard_indices = []
        styles_text = []
        bases_text = []
        for s in styles:
            styles_text.append(s.name)
        for b in bases:
            bases_text.append(b.name)

        s1, s1i = pick(styles_text, 'Choose your first discarded style', '=>')
        discard_indices.append(s1i)
        styles_text.pop(s1i)
        s2, s2i = pick(styles_text, 'Choose your second discarded style', '=>')
        if s2i >= s1i:
            s2i += 1
        discard_indices.append(s2i)

        b1, b1i = pick(bases_text, 'Choose your first discarded base', '=>')
        discard_indices.append(b1i)
        bases_text.pop(b1i)
        b2, b2i = pick(bases_text, 'Choose your second discarded base', '=>')
        if b2i >= b1i:
            b2i += 1
        discard_indices.append(b2i)
        return discard_indices

    def get_selection(self, av_styles, av_bases, state):
        ctx = state_string_cli(state)
        styles_text = []
        bases_text = []
        for i in av_styles:
            styles_text.append(state.p.character.styles[i].name)
        for j in av_bases:
            bases_text.append(state.p.character.bases[j].name)
        s, si = pick(styles_text, ctx + 'Select a style to play', '=>')
        b, bi = pick(bases_text, ctx + 'Select a base to play', '=>')
        return av_styles[si], av_bases[bi]

    def get_new_base(self, av_bases, state):
        ctx = state_string_cli(state)
        bases_text = []
        for i in av_bases:
            bases_text.append(state.p.character.bases[i].name)
        b, bi = pick(bases_text, ctx + 'CLASH Select a new base to play', '=>')
        return av_bases[bi]

    def get_ante(self, state):
        ctx = state_string_cli(state)
        ante_opts_text = ['None', 'Finisher']
        ante, antei = pick(ante_opts_text, ctx + 'Your turn to ante', '=>')
        return ante

    # def get_behaviors(self, possible, state):
    #     def get_behavior(opts, last):
    #     # can't simulate state, as opponent will get opportunity to act
    #     # in some cases...  need to get behaviors one at a time
    #     simulated =
    #     ctx = state_string_cli(state)
    #     chosen = []
    #     done = []
    #     while len(chosen) < len(possible):
    #         remaining = [x for x in range(len(possible)) if x not in done]
    #         if len(chosen) == len(possible) - 1:
    #             chosen.append(get_behavior(possible[remaining[0]], True))
    #         else:
    #             act, act_i = pick(remaining, ctx + 'Select an action', '=>')
    #             selected = get_behavior(possible[int(act)], False)
    #             if selected is not None:
    #                 done.append(int(act))
    #                 chosen.append(selected)
    #     return chosen
