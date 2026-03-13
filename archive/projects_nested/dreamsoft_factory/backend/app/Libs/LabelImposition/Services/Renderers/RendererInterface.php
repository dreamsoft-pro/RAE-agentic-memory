<?php

namespace DreamSoft\Libs\LabelImposition\Services\Renderers;

interface RendererInterface
{
    public function render(): array;

    public function rotate(string $imageUrl, int $rotate = 0): string;

    public function getSize(string $filePath): array;
}
