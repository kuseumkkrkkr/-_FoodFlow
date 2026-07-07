import 'package:flutter/material.dart';

class AppCard extends StatelessWidget {
  const AppCard({
    super.key,
    required this.title,
    required this.child,
    this.trailing,
  });

  final String title;
  final Widget child;
  final Widget? trailing;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                ),
                if (trailing != null) trailing!,
              ],
            ),
            const SizedBox(height: 12),
            child,
          ],
        ),
      ),
    );
  }
}

class InfoBlock extends StatelessWidget {
  const InfoBlock({
    super.key,
    required this.title,
    this.lines = const [],
    this.chips = const [],
  });

  final String title;
  final List<String> lines;
  final List<String> chips;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(title, style: const TextStyle(fontWeight: FontWeight.w700)),
          const SizedBox(height: 6),
          if (lines.isNotEmpty)
            ...lines.map(
              (line) => Padding(
                padding: const EdgeInsets.only(bottom: 5),
                child: Text(line),
              ),
            ),
          if (chips.isNotEmpty)
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: chips.map((chip) => StatusChip(label: chip)).toList(),
            ),
        ],
      ),
    );
  }
}

class FilterMenu extends StatelessWidget {
  const FilterMenu({
    super.key,
    required this.label,
    required this.value,
    required this.entries,
    required this.onChanged,
  });

  final String label;
  final String value;
  final Map<String, String> entries;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 168,
      child: DropdownMenu<String>(
        initialSelection: value.isEmpty ? '' : value,
        label: Text(label),
        dropdownMenuEntries: [
          const DropdownMenuEntry(value: '', label: '전체'),
          ...entries.entries.map(
            (entry) => DropdownMenuEntry(value: entry.key, label: entry.value),
          ),
        ],
        onSelected: (selected) => onChanged(selected ?? ''),
      ),
    );
  }
}

class FindingTile extends StatelessWidget {
  const FindingTile({super.key, required this.finding});

  final Map<String, dynamic> finding;

  @override
  Widget build(BuildContext context) {
    final severity = finding['severity'] as String? ?? 'YELLOW';
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 8),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: toneFor(severity).background,
        borderRadius: BorderRadius.circular(8),
        border: Border(
          left: BorderSide(color: toneFor(severity).foreground, width: 4),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          StatusChip(
            label: '$severity · ${finding['rule_id']}',
            tone: toneFor(severity),
          ),
          const SizedBox(height: 6),
          Text(finding['message'] as String? ?? ''),
          const SizedBox(height: 4),
          Text(
            '필요 증빙: ${finding['required_evidence']}',
            style: const TextStyle(fontSize: 12),
          ),
        ],
      ),
    );
  }
}

class StatusChip extends StatelessWidget {
  const StatusChip({
    super.key,
    required this.label,
    this.tone = ChipTone.neutral,
  });

  final String label;
  final ChipTone tone;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: tone.background,
        borderRadius: BorderRadius.circular(999),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: tone.foreground,
          fontSize: 12,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}

class ChipTone {
  const ChipTone(this.background, this.foreground);

  final Color background;
  final Color foreground;

  static const neutral = ChipTone(Color(0xffeef2ef), Color(0xff39473f));
  static const green = ChipTone(Color(0xffeaf7ef), Color(0xff14794f));
  static const yellow = ChipTone(Color(0xfffff7df), Color(0xffa16207));
  static const red = ChipTone(Color(0xfffff1f0), Color(0xffb42318));
}

ChipTone toneFor(String? value) {
  if (value == 'RED' || value == 'needs_review') {
    return ChipTone.red;
  }
  if (value == 'YELLOW') {
    return ChipTone.yellow;
  }
  if (value == 'GREEN' || value == 'brief_ready' || value == 'ready_to_send') {
    return ChipTone.green;
  }
  return ChipTone.neutral;
}

class ErrorBanner extends StatelessWidget {
  const ErrorBanner({super.key, required this.error});

  final String error;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: const Color(0xfffff1f0),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: const Color(0xffffc9c5)),
      ),
      child: Text(error, style: const TextStyle(color: Color(0xffb42318))),
    );
  }
}

List<Widget> separated(List<Widget> items, double gap) {
  if (items.isEmpty) return items;
  final output = <Widget>[];
  for (var i = 0; i < items.length; i++) {
    output.add(items[i]);
    if (i != items.length - 1 && gap > 0) {
      output.add(SizedBox(width: gap, height: gap));
    }
  }
  return output;
}
