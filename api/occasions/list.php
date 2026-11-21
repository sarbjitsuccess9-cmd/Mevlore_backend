<?php
declare(strict_types=1);

require_once dirname(__DIR__, 2) . '/includes/db.php';
require_once dirname(__DIR__, 2) . '/includes/response.php';
require_once dirname(__DIR__, 2) . '/services/ThemeEngineService.php';

MelvoreResponse::requireMethod('GET');

try {
    $pdo = MelvoreDB::pdo();
    $occasions = [];
    if (MelvoreDB::tableExists('app_occasions')) {
        $stmt = $pdo->query('SELECT * FROM app_occasions ORDER BY priority DESC, occasion_id ASC');
        foreach ($stmt->fetchAll() as $row) {
            $occasions[] = [
                'occasion_id' => (int)$row['occasion_id'],
                'slug' => (string)$row['slug'],
                'name' => (string)$row['name'],
                'eyebrow' => (string)($row['eyebrow'] ?? ''),
                'headline' => (string)($row['headline'] ?? ''),
                'subtitle' => (string)($row['subtitle'] ?? ''),
                'occasion_type' => (string)($row['occasion_type'] ?? 'festival'),
                'motif_key' => (string)($row['motif_key'] ?? 'confetti'),
                'primary_color' => (string)$row['primary_color'],
                'accent_color' => (string)$row['accent_color'],
                'background_color' => (string)$row['background_color'],
                'is_active' => ((int)$row['is_active']) === 1,
                'priority' => (int)$row['priority'],
                'start_date' => $row['start_date'] ?? null,
                'end_date' => $row['end_date'] ?? null,
            ];
        }
    }
    MelvoreResponse::ok(['occasions' => $occasions], 'Occasions loaded');
} catch (Throwable $e) {
    MelvoreResponse::error('Unable to load occasions.', 'SERVER_ERROR', 500);
}
